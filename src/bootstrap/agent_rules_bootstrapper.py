"""
Agent Rules Bootstrapper for initializing rule repositories from multiple sources.
"""

import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..config.bootstrap_configuration import BootstrapConfiguration
from ..config.environment_parser import EnvironmentConfigurationParser
from ..factory.rule_loader_factory import RuleLoaderFactory
from ..repository.agent_rule_repository import AgentRuleRepository

@dataclass
class LoadResult:
    """
    Result of loading rules from a specific source.
    """
    source_index: int
    source_type: str
    source_path: Optional[str] = None
    status: str = "pending"  # pending, success, failed
    rules_loaded: int = 0
    error: Optional[str] = None
    load_time_seconds: float = 0.0
    
    def is_success(self) -> bool:
        """Check if the load was successful."""
        return self.status == "success"
    
    def is_failed(self) -> bool:
        """Check if the load failed."""
        return self.status == "failed"

@dataclass
class BootstrapStats:
    """
    Statistics from the bootstrap process.
    """
    total_sources: int
    successful_sources: int
    failed_sources: int
    total_rules_loaded: int
    total_time_seconds: float
    source_results: List[LoadResult]
    
    def get_success_rate(self) -> float:
        """Get the success rate as a percentage."""
        if self.total_sources == 0:
            return 0.0
        return (self.successful_sources / self.total_sources) * 100
    
    def get_failed_sources(self) -> List[LoadResult]:
        """Get list of failed source results."""
        return [result for result in self.source_results if result.is_failed()]
    
    def get_successful_sources(self) -> List[LoadResult]:
        """Get list of successful source results."""
        return [result for result in self.source_results if result.is_success()]

class AgentRulesBootstrapper:
    """
    Bootstrapper for initializing Agent Rules repositories from multiple sources.
    
    Supports configuration via environment variables with indexed pattern:
    RulesLoaderOptions:0:SourceType = YamlFile
    RulesLoaderOptions:0:Path = ./rules
    RulesLoaderOptions:1:SourceType = YamlFile  
    RulesLoaderOptions:1:Path = c:/git/rules
    """
    
    def __init__(self, config: BootstrapConfiguration):
        """
        Initialize bootstrapper with configuration.
        
        Args:
            config: Bootstrap configuration
        """
        self.config = config
        self.factory = RuleLoaderFactory()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Results from bootstrap process
        self.load_results: List[LoadResult] = []
        self.bootstrap_stats: Optional[BootstrapStats] = None
    
    @classmethod
    def from_environment(cls) -> 'AgentRulesBootstrapper':
        """
        Create bootstrapper from environment variables.
        
        Returns:
            AgentRulesBootstrapper configured from environment
            
        Raises:
            ValueError: If environment configuration is invalid
        """
        parser = EnvironmentConfigurationParser()
        config = parser.parse_bootstrap_configuration()
        return cls(config)
    
    def bootstrap(self) -> AgentRuleRepository:
        """
        Bootstrap repository from all configured sources.
        
        Returns:
            Initialized AgentRuleRepository with rules from all sources
        """
        start_time = time.time()
        repository = AgentRuleRepository()
        self.load_results = []
        
        self.logger.info(f"Starting bootstrap with {len(self.config.sources)} sources")
        
        # Load from each source
        for i, source_config in enumerate(self.config.sources):
            result = self._load_from_source(i, source_config, repository)
            self.load_results.append(result)
        
        # Generate statistics
        end_time = time.time()
        self.bootstrap_stats = self._generate_stats(start_time, end_time)
        
        # Log summary
        self._log_bootstrap_summary()
        
        return repository
    
    def _load_from_source(self, index: int, source_config, repository: AgentRuleRepository) -> LoadResult:
        """
        Load rules from a single source.
        
        Args:
            index: Source index
            source_config: Source configuration
            repository: Repository to load rules into
            
        Returns:
            LoadResult with details of the operation
        """
        result = LoadResult(
            source_index=index,
            source_type=source_config.source_type,
            source_path=getattr(source_config, 'path', None)
        )
        
        start_time = time.time()
        
        try:
            self.logger.info(f"Loading source {index}: {source_config.source_type}")
            
            # Validate source if validation is enabled
            if self.config.validation_enabled:
                source_config.validate()
            
            # Create loader and load rules
            loader = self.factory.create_loader(source_config)
            rules_loaded = loader.load_rules_to_repository(repository)
            
            # Success
            result.status = "success"
            result.rules_loaded = rules_loaded
            result.load_time_seconds = time.time() - start_time
            
            self.logger.info(f"Source {index} loaded {rules_loaded} rules successfully")
            
        except Exception as e:
            # Failure
            result.status = "failed"
            result.error = str(e)
            result.load_time_seconds = time.time() - start_time
            
            self.logger.error(f"Source {index} failed: {e}")
            
            # Continue with other sources unless configured otherwise
            
        return result
    
    def _generate_stats(self, start_time: float, end_time: float) -> BootstrapStats:
        """
        Generate bootstrap statistics.
        
        Args:
            start_time: Bootstrap start timestamp
            end_time: Bootstrap end timestamp
            
        Returns:
            BootstrapStats with summary information
        """
        successful_results = [r for r in self.load_results if r.is_success()]
        failed_results = [r for r in self.load_results if r.is_failed()]
        
        total_rules = sum(r.rules_loaded for r in successful_results)
        
        return BootstrapStats(
            total_sources=len(self.load_results),
            successful_sources=len(successful_results),
            failed_sources=len(failed_results),
            total_rules_loaded=total_rules,
            total_time_seconds=end_time - start_time,
            source_results=self.load_results.copy()
        )
    
    def _log_bootstrap_summary(self) -> None:
        """Log summary of bootstrap results."""
        if not self.bootstrap_stats:
            return
        
        stats = self.bootstrap_stats
        
        self.logger.info(f"Bootstrap completed in {stats.total_time_seconds:.2f}s")
        self.logger.info(f"Sources: {stats.successful_sources}/{stats.total_sources} successful")
        self.logger.info(f"Total rules loaded: {stats.total_rules_loaded}")
        
        if stats.failed_sources > 0:
            self.logger.warning(f"{stats.failed_sources} sources failed to load")
            for failed_result in stats.get_failed_sources():
                self.logger.warning(f"  Source {failed_result.source_index}: {failed_result.error}")
    
    def _setup_logging(self) -> None:
        """Setup logging based on configuration."""
        log_level = getattr(logging, self.config.log_level, logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def validate_sources(self) -> Dict[str, any]:
        """
        Validate all source configurations without loading.
        
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "sources": []
        }
        
        for i, source_config in enumerate(self.config.sources):
            source_result = {
                "index": i,
                "source_type": source_config.source_type,
                "valid": True,
                "errors": []
            }
            
            try:
                source_config.validate()
                
                # Try creating loader
                self.factory.create_loader(source_config)
                
            except Exception as e:
                source_result["valid"] = False
                source_result["errors"].append(str(e))
                validation_result["valid"] = False
                validation_result["errors"].append(f"Source {i}: {e}")
            
            validation_result["sources"].append(source_result)
        
        return validation_result
    
    def get_bootstrap_stats(self) -> Optional[BootstrapStats]:
        """
        Get bootstrap statistics.
        
        Returns:
            BootstrapStats if bootstrap has been run, None otherwise
        """
        return self.bootstrap_stats
    
    def get_load_results(self) -> List[LoadResult]:
        """
        Get detailed load results.
        
        Returns:
            List of LoadResult objects
        """
        return self.load_results.copy()
    
    def print_configuration(self) -> None:
        """Print current configuration for debugging."""
        print(f"Bootstrap Configuration:")
        print(f"  Sources: {len(self.config.sources)}")
        print(f"  Validation enabled: {self.config.validation_enabled}")
        print(f"  Log level: {self.config.log_level}")
        print()
        
        for i, source in enumerate(self.config.sources):
            print(f"  Source {i}: {source}")
        print()
    
    def print_results(self) -> None:
        """Print bootstrap results for debugging."""
        if not self.bootstrap_stats:
            print("No bootstrap results available - run bootstrap() first")
            return
        
        stats = self.bootstrap_stats
        print(f"Bootstrap Results:")
        print(f"  Total time: {stats.total_time_seconds:.2f}s")
        print(f"  Success rate: {stats.get_success_rate():.1f}%")
        print(f"  Rules loaded: {stats.total_rules_loaded}")
        print()
        
        for result in self.load_results:
            status_icon = "✓" if result.is_success() else "✗"
            print(f"  {status_icon} Source {result.source_index} ({result.source_type}): ", end="")
            
            if result.is_success():
                print(f"{result.rules_loaded} rules in {result.load_time_seconds:.2f}s")
            else:
                print(f"FAILED - {result.error}")
        print()
    
    def __str__(self) -> str:
        return f"AgentRulesBootstrapper({len(self.config.sources)} sources)"
    
    def __repr__(self) -> str:
        return f"AgentRulesBootstrapper(config={self.config})"

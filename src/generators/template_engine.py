"""Template rendering engine using Jinja2."""

import os
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
from ..models.api_spec import APISpecification
from ..models.sdk_config import SDKConfig


class TemplateEngine:
    """Engine for rendering Jinja2 templates."""
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the template engine.
        
        Args:
            templates_dir: Path to templates directory. If None, uses default.
        """
        if templates_dir is None:
            # Default to templates/typescript directory
            project_root = Path(__file__).parent.parent.parent
            templates_dir = str(project_root / "templates" / "typescript")
        
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Context dictionary for rendering
            
        Returns:
            Rendered template string
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_errors(self, api_spec: APISpecification) -> str:
        """Render errors.ts template."""
        context = {
            "api_name": api_spec.api_name,
        }
        return self.render_template("errors.ts.jinja2", context)
    
    def render_retry(self, sdk_config: SDKConfig) -> str:
        """Render retry.ts template."""
        context = {
            "api_name": sdk_config.package_name,
            "retry_config": {
                "max_retries": sdk_config.retry_config.max_retries,
                "base_delay": sdk_config.retry_config.base_delay,
                "max_delay": sdk_config.retry_config.max_delay,
                "retryable_status_codes": sdk_config.retry_config.retryable_status_codes,
            }
        }
        return self.render_template("retry.ts.jinja2", context)
    
    def render_rate_limiter(self, sdk_config: SDKConfig) -> str:
        """Render rateLimiter.ts template."""
        context = {
            "api_name": sdk_config.package_name,
            "rate_limit_config": {
                "requests_per_second": sdk_config.rate_limit_config.requests_per_second,
                "burst_allowance": sdk_config.rate_limit_config.burst_allowance,
            }
        }
        return self.render_template("rateLimiter.ts.jinja2", context)
    
    def render_logger(self) -> str:
        """Render logger.ts template."""
        return self.render_template("logger.ts.jinja2", {})
    
    def render_client(
        self,
        api_spec: APISpecification,
        sdk_config: SDKConfig,
        endpoint_methods: str
    ) -> str:
        """Render client.ts template."""
        # Convert API name to class name (e.g., "My API" -> "MyAPI")
        api_name_class = api_spec.api_name.replace(" ", "").replace("-", "")
        
        context = {
            "api_name": api_spec.api_name,
            "api_name_class": api_name_class,
            "auth_type": api_spec.auth_type.value,
            "global_headers": api_spec.global_headers,
            "enable_retry_logic": sdk_config.enable_retry_logic,
            "enable_rate_limiting": sdk_config.enable_rate_limiting,
            "endpoint_methods": endpoint_methods,
        }
        return self.render_template("client.ts.jinja2", context)
    
    def render_index(
        self,
        api_spec: APISpecification,
        sdk_config: SDKConfig
    ) -> str:
        """Render index.ts template."""
        api_name_class = api_spec.api_name.replace(" ", "").replace("-", "")
        
        context = {
            "api_name": api_spec.api_name,
            "api_name_class": api_name_class,
            "enable_retry_logic": sdk_config.enable_retry_logic,
            "enable_rate_limiting": sdk_config.enable_rate_limiting,
        }
        return self.render_template("index.ts.jinja2", context)
    
    def render_package_json(
        self,
        api_spec: APISpecification,
        sdk_config: SDKConfig
    ) -> str:
        """Render package.json template."""
        context = {
            "package_name": sdk_config.package_name,
            "version": sdk_config.version,
            "author": sdk_config.author,
            "license": sdk_config.license.value,
            "api_name": api_spec.api_name,
        }
        return self.render_template("package.json.jinja2", context)
    
    def render_tsconfig(self) -> str:
        """Render tsconfig.json template."""
        return self.render_template("tsconfig.json.jinja2", {})
    
    def render_gitignore(self) -> str:
        """Render .gitignore template."""
        return self.render_template("gitignore.jinja2", {})
    
    def render_readme(
        self,
        api_spec: APISpecification,
        sdk_config: SDKConfig,
        usage_examples: str = ""
    ) -> str:
        """Render README.md template."""
        api_name_class = api_spec.api_name.replace(" ", "").replace("-", "")
        
        context = {
            "api_name": api_spec.api_name,
            "api_name_class": api_name_class,
            "package_name": sdk_config.package_name,
            "base_url": str(api_spec.base_url),
            "auth_type": api_spec.auth_type.value,
            "license": sdk_config.license.value,
            "enable_retry_logic": sdk_config.enable_retry_logic,
            "enable_rate_limiting": sdk_config.enable_rate_limiting,
            "usage_examples": usage_examples,
        }
        return self.render_template("README.md.jinja2", context)
    
    def render_all_base_files(
        self,
        api_spec: APISpecification,
        sdk_config: SDKConfig
    ) -> Dict[str, str]:
        """
        Render all base template files (non-LLM generated).
        
        Args:
            api_spec: API specification
            sdk_config: SDK configuration
            
        Returns:
            Dictionary mapping file paths to rendered content
        """
        files = {}
        
        # Always include these files
        files["src/errors.ts"] = self.render_errors(api_spec)
        files["src/utils/logger.ts"] = self.render_logger()
        files["package.json"] = self.render_package_json(api_spec, sdk_config)
        files["tsconfig.json"] = self.render_tsconfig()
        files[".gitignore"] = self.render_gitignore()
        
        # Conditional files based on SDK config
        if sdk_config.enable_retry_logic:
            files["src/utils/retry.ts"] = self.render_retry(sdk_config)
        
        if sdk_config.enable_rate_limiting:
            files["src/utils/rateLimiter.ts"] = self.render_rate_limiter(sdk_config)
        
        return files

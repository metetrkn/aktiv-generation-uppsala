# =============================================================================
# Component: Code Quality
# Version: $(VERSION)
# Description: Code quality checks and formatting
# Dependencies: poetry, black, isort, flake8, bandit, safety, pylint, vulture, mypy

# Exclude patterns for all tools
EXCLUDE_DIRS := .git,myenv,.myenv,.env,env,venv,.venv,.pytest_cache,.coverage,htmlcov,node_modules,staticfiles,media,*/migrations/*,*/management/*,*/tests/*

# =============================================================================

.PHONY: quality-format quality-lint quality-check-all

# -----------------------------------------------------------------------------
# Code Quality
# -----------------------------------------------------------------------------
quality-format:
	@echo "🎨 Formatting code..."
	poetry run black apps/core apps/mail apps/photo
	poetry run isort apps/core apps/mail apps/photo

quality-lint:
	@echo "🔍 Running linters..."
	poetry run black --check apps/core apps/mail apps/photo
	poetry run isort --check-only apps/core apps/mail apps/photo
	poetry run flake8 apps/core apps/mail apps/photo
	poetry run pylint apps/core apps/mail apps/photo --recursive=y
	poetry run vulture apps/core apps/mail apps/photo
	poetry run mypy apps/core apps/mail apps/photo

# Run all quality checks
quality-check-all: quality-lint
	@echo "✅ All quality checks passed!"

help-quality-lint:
	@echo "\n$(CYAN)Command: $(YELLOW)make quality-lint$(NC)"
	@echo "$(BLUE)Description:$(NC) Run all linters"
	@echo "$(BLUE)Usage:$(NC) make quality-lint"
	@echo "$(BLUE)Example:$(NC) make quality-lint"
	@echo "$(BLUE)Notes:$(NC)"
	@echo "This command will:"
	@echo "- Run pre-commit hooks for all quality checks"
	@echo ""

help-quality-format:
	@echo "\n$(CYAN)Command: $(YELLOW)make quality-format$(NC)"
	@echo "$(BLUE)Description:$(NC) Format code automatically"
	@echo "$(BLUE)Usage:$(NC) make quality-format"
	@echo "$(BLUE)Example:$(NC) make quality-format"
	@echo "$(BLUE)Notes:$(NC)"
	@echo "This command will:"
	@echo "- Format code with black"
	@echo "- Sort imports with isort"
	@echo ""

help-quality-check-all:
	@echo "\n$(CYAN)Command: $(YELLOW)make quality-check-all$(NC)"
	@echo "$(BLUE)Description:$(NC) Run all code quality checks"
	@echo "$(BLUE)Usage:$(NC) make quality-check-all"
	@echo "$(BLUE)Example:$(NC) make quality-check-all"
	@echo "$(BLUE)Notes:$(NC)"
	@echo "This command will:"
	@echo "- Format code"
	@echo "- Run all linters"
	@echo "- Show comprehensive results"
	@echo ""

# Nimship Agent

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Repo](https://img.shields.io/badge/GitHub-nimship--agent-blue?logo=github)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A multi-agent collaborative development framework built on phidata, supporting configurable workflows and intelligent toolchains**

[Features](#main-features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](CONTRIBUTING.md) • [License](LICENSE)

</div>

---

## Main Features

### 🤖 Multi-Agent Collaboration System
- **Pre-configured Professional Roles**: Product Manager, Tech Lead, Senior Engineer, QA Engineer
- **Workflow-based Collaboration**: Clear state transitions and task flow
- **Well-defined Role Responsibilities**: Each Agent focuses on specific domains, improving collaboration efficiency

### ⚙️ Flexible Configuration System
- **JSON Configuration Files**: Define agents and workflows through configuration files without code changes
- **Standardized Validation**: Ensures correctness and completeness of configuration files
- **Multi-model Support**: Supports multiple language models (via phidata), including AWS Bedrock (Claude)

### 🛠️ Tool Integration
- **Core Tools**:
  - `FileManager`: Unified file operation interface
  - `DevOps`: Environment management and deployment operations
  - `DuckDuckGo`: Web search capabilities
- **Extensible Architecture**: Tool configuration separated from implementation, easy to extend new tools
- **Permission Control**: Supports tool-level permission management

### 📋 Workflow Management
- **State-driven Engine**: Workflow execution based on state machines
- **Configurable State Transitions**: Define state transition rules through configuration files
- **Complete Validation**: Ensures correct workflow execution
- **Serial and Parallel Execution**: Supports complex workflow scenarios

## Project Structure

```
nimship-agent/
├── agents/                    # Agent implementations
│   └── base_agent.py         # Agent base class
├── config/                   # Configuration files
│   ├── agents/              # Agent configurations
│   ├── workflows/           # Workflow configurations
│   ├── tools/               # Tool configurations
│   └── system.config.json   # System configuration
├── docs/                     # Documentation
│   ├── workflow_developer.md
│   └── AGENT_DESIGN.md
├── tests/                    # Test cases
│   ├── integration/         # Integration tests
│   └── tools/               # Tool tests
├── tools/                    # Tool implementations
├── utils/                    # Utility functions
├── workflows/                # Workflow implementations
├── main.py                   # Main entry point
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
```

## Quick Start

### Requirements

- Python 3.9+
- Virtual environment management tool (recommended: `venv`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ovenzeze/nimship-agent.git
   cd nimship-agent
   ```

2. **Create a virtual environment**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   
   Create a `.env` file and configure necessary environment variables:
   ```bash
   # AWS configuration (for Bedrock)
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   
   # Phidata API Key (if needed)
   PHI_API_KEY=your_phi_api_key
   ```

### Usage

#### CLI Mode

```bash
python main.py
```

#### Run with a specific workflow

```bash
python main.py --workflow developer
```

#### Web UI Mode

```bash
python main.py --mode ui
```

## Development Guide

### Agent Configuration Specification

- **Configuration file location**: `config/agents/` directory
- **File suffix**: `.agent.json`
- **Required fields**: `name`, `description`, `model`, `tools`

Example configuration structure:
```json
{
  "name": "engineer",
  "description": "Senior Engineer",
  "model": "anthropic.claude-instant-v1",
  "tools": ["file_manager", "git"]
}
```

### Workflow Configuration Specification

- **Configuration file location**: `config/workflows/` directory
- **File suffix**: `.workflow.json`
- **Required definitions**: State transitions and conditions

### Testing Specification

- **Unit tests**: `tests/` directory
- **Integration tests**: `tests/integration/` directory
- **Run tests**:
  ```bash
  pytest tests/
  ```

For more development guidelines, please refer to [DEV_GUIDE.md](DEV_GUIDE.md)

## Documentation

- 📖 [Workflow Development Guide](docs/workflow_developer.md) - Learn how to create and configure workflows
- 📖 [Agent Design Document](docs/AGENT_DESIGN.md) - Agent architecture and design philosophy
- 📖 [Developer Guide](DEV_GUIDE.md) - Development environment setup and common tasks
- 📖 [Test Architecture](tests/test_design.md) - Testing framework and best practices

## Development Status

The project is currently in active development:

- ✅ Completed basic configuration system
- ✅ Completed workflow framework design
- ✅ Implemented core functional modules
- 🚧 Improving test coverage
- 🚧 Performance optimization
- 📋 Documentation improvements

## Notes

### Remote Development Environment Configuration

To use remote development features, you need to configure:

- VSCode Server
- SSH key authentication
- Git and GitHub configuration

### Dependencies

Main dependencies:
- `phidata` - AI application framework
- `boto3` - AWS SDK (for Bedrock)
- `paramiko` - SSH connections (for remote operations)
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management
- `rich` - Terminal output formatting

## Contributing

We welcome all forms of contributions! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

Quick start:
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Built on the [phidata](https://github.com/phidatahq/phidata) framework
- Thanks to all contributors for their support

---

<div align="center">

**If this project helps you, please give it a ⭐ Star!**

Made with ❤️ by the Nimship Agent Team

</div>

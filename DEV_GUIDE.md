# Nimship Agent Developer Guide

Nimship Agent is a configurable AI agent framework built on phidata. This guide helps developers understand the project structure and how to make common modifications.

## Core Components

1. **Agent Implementation** (`agents/base_agent.py`)
- Contains `NimshipAgent` class extending phidata's `Agent`
- Handles agent initialization and execution logic
- Modify here to change core agent behavior

2. **Model Management** (`utils/model_factory.py`)
- Responsible for loading and configuring language models
- Extend here to add new model support
- Utilizes phidata's built-in model capabilities

3. **Configuration System**
- `config/system.config.json`: System-level configuration
- `config/*.agent.json`: Individual agent configurations
- Customize agent behavior through configuration files

4. **Entry Points**
- `run_agent.py`: Command-line interface
- `playground.py`: Web UI interface
- Modify these files to change interaction methods

## Common Development Tasks

1. **Adding New Model Support**
- Check if phidata already supports the model
- If supported, only need to specify in agent config
- For customization, modify `model_factory.py`

2. **Integrating New Tools**
- Add tool configuration in agent config file
- Reference tool configuration examples in `web.agent.json`

3. **Modifying Agent Behavior**
- Edit `agents/base_agent.py`
- Override parent methods or add new functionality

4. **Custom Storage**
- Default uses SQLite storage
- Modify storage config in agent config file
- Can extend to support other storage types

5. **UI Customization**
- Modify `playground.py` to change Web UI
- Utilize phidata's Playground component features

6. **Remote Development Testing**
- Use `tests/test_remote_development.py` for remote development tests
- Ensure proper configuration of remote server details in `.env` file
- Run tests using pytest and check for skipped tests due to missing dependencies

## Project Structure

```
nimship-agent/
├── agents/                 # Agent implementations
│   └── base_agent.py      # Base Agent class
├── utils/                 # Utilities
│   └── model_factory.py   # Model loading utility
├── config/                # Configurations
│   ├── system.config.json # System config
│   └── *.agent.json      # Agent configs
├── tests/                 # Test files
│   └── test_remote_development.py # Remote development tests
├── run_agent.py          # CLI entry
└── playground.py         # Web UI entry
```

## Development Workflow

1. **Creating New Agents**
- Create new config file in `config/`
- Use existing `NimshipAgent` class or extend it
- Configure model, tools, and storage options

2. **Extending Functionality**
- Inherit from `NimshipAgent` for custom behavior
- Add new utility functions in `utils/`
- Maintain configuration-driven approach

3. **Testing and Debugging**
- Use CLI for quick tests
- Utilize Playground for interactive testing
- Run pytest for comprehensive testing, including remote development tests
- Monitor agent behavior through logs
- Check for skipped tests and ensure all dependencies are installed

## Extension Guidelines

1. **Adding Features**
- Prefer configuration-based implementation
- Start with `NimshipAgent` inheritance
- Maintain phidata compatibility

2. **Performance Optimization**
- Review initialization logic in `base_agent.py`
- Consider optimizing model loading
- Extend caching mechanisms

3. **Code Organization**
- Keep configuration and code separate
- Prioritize inheritance for new features
- Leverage phidata built-in functionality

## Important Notes

1. Heavy dependency on phidata library - refer to phidata documentation
2. Maintain backward compatibility when modifying core features
3. Configuration-driven design requires stable config structure
4. Ensure all dependencies are installed before running tests

The framework is designed to enable rapid creation and customization of AI agents through configuration, while maintaining code maintainability and extensibility. Most common requirements can be implemented through configuration files, with code modifications needed only for deep customization.

## Dependencies

Core dependencies:
- phidata: AI application framework
- fastapi: Web services
- sqlalchemy: Data storage
- pytest: Testing framework
- paramiko: SSH operations for remote development tests
- requests: HTTP operations for remote development tests

This modular, configuration-driven architecture makes it easy for developers to create, modify, and extend AI agents while leveraging the robust capabilities of the phidata framework.

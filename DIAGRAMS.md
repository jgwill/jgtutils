# Class Diagrams

```mermaid
classDiagram
    class FXTrade
    class FXOrder
    class FXTrades {
        +trades
        +add_trade(trade_data)
        +to_dict()
        +tojson()
        +toyaml()
    }
    class FXOrders {
        +orders
        +add_order(order_data)
        +to_dict()
        +tojson()
        +toyaml()
    }
    class FXTransactWrapper {
        +trades: FXTrades
        +orders: FXOrders
        +add_trade(trade)
        +add_order(order)
        +find_matching_trade(order)
    }
    class FXTransactDataHelper
    FXTrades --> FXTrade
    FXOrders --> FXOrder
    FXTransactWrapper --> FXTrades
    FXTransactWrapper --> FXOrders
    FXTransactDataHelper --> FXTransactWrapper
```

These classes live in `jgtutils/FXTransact.py` and handle trade and order data, saving and loading them as JSON or YAML.

---

## Configuration Flow

```mermaid
graph TD
    A["config.json"] -->|"read by jgtcommon.readconfig()"| B(("Credentials dict"))
    C["settings.json, settings.yml, jgt.yml, _config.yml"] -->|"merged by jgtcommon.load_settings()"| D(("Settings dict"))
    E["Environment variables"] --> D
    F["-ls/--settings CLI option"] --> D
    B -->|"export_env=True"| G["Environment variables"]
    D -->|"jgtset CLI can export to .env"| H[".env file"]
```

- `config.json` is loaded in a specific order (see CONFIGURATION.md).
- `settings.json` and related files are merged, with later sources overriding earlier ones.
- Both can be exported to environment variables for use in scripts or shells.

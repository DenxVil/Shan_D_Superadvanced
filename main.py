import os
import sys
import traceback

def safe_import(module_path, object_name=None):
    """
    Attempts to import a module and optionally an object from it.
    Exits with a clear error if not found.
    """
    try:
        module = __import__(module_path, fromlist=[object_name] if object_name else [])
        if object_name:
            return getattr(module, object_name)
        return module
    except (ImportError, AttributeError) as e:
        sys.exit(f"Failed to import '{object_name or module_path}'.\nError: {e}\n"
                 f"Check that your src/ directory and modules are present and valid.")
        
def validate_config(cfg):
    # Minimal validation for required structure
    try:
        _ = cfg.telegram.token
    except AttributeError:
        sys.exit("Config error: cfg.telegram.token missing. "
                 "Check your config loader and structure.")
    return True

def main():
    # --- 1. Read Telegram credentials explicitly from environment ---
    api_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not api_token:
        sys.exit("Error: Missing env var TELEGRAM_BOT_TOKEN. Please set it and rerun.")

    # --- 2. Import modules safely ---
    TelegramBot = safe_import("src.TelegramX.telegram_bot", "TelegramBot")
    ConversationFlow = safe_import("src.core.conversation_flow", "ConversationFlow")
    EmotionEngine = safe_import("src.core.emotion_engine", "EmotionEngine")
    ErrorHandler = safe_import("src.core.error_handler", "ErrorHandler")
    LearningEngine = safe_import("src.core.learning_engine", "LearningEngine")
    MemoryManager = safe_import("src.core.memory_manager", "MemoryManager")
    ModelManager = safe_import("src.core.model_manager", "ModelManager")
    Personality = safe_import("src.core.personality", "Personality")
    ReasoningEngine = safe_import("src.core.reasoning_engine", "ReasoningEngine")
    ShanDEnhanced = safe_import("src.core.shan_d_enhanced", "ShanDEnhanced")
    AnalyticsEngine = safe_import("src.storage.analytics_engine", "AnalyticsEngine")
    UserDataManager = safe_import("src.storage.user_data_manager", "UserDataManager")
    load_config = safe_import("src.utils.config", "load_config")
    advanced_security_scan = safe_import("src.utils.advanced_security", "advanced_security_scan")

    # --- 3. Load config and validate ---
    cfg = load_config()
    # Always override with env token for safety
    try:
        cfg.telegram.token = api_token
    except Exception:
        sys.exit("Config object does not have 'telegram' or 'token'. Check your config structure.")
    validate_config(cfg)

    # --- 4. Initialize storage & analytics ---
    try:
        user_db = UserDataManager(cfg)
        analytics = AnalyticsEngine()
    except Exception as e:
        sys.exit(f"Failed to initialize storage/analytics: {e}")

    # --- 5. Initialize core engines ---
    try:
        memory = MemoryManager(cfg)
        model_mgr = ModelManager(cfg)
        learning = LearningEngine(cfg)
        reasoning = ReasoningEngine(cfg)
        personality = Personality(cfg)
        emotion = EmotionEngine(cfg)
        convo_flow = ConversationFlow(
            memory=memory,
            model_manager=model_mgr,
            personality=personality,
            emotion_engine=emotion,
            learning_engine=learning,
            analytics_engine=analytics,
        )
        enhanced = ShanDEnhanced(convo_flow, cfg)
    except Exception as e:
        sys.exit(f"Core engine initialization failed: {e}")

    # --- 6. Setup error handling ---
    try:
        error_handler = ErrorHandler()
    except Exception as e:
        sys.exit(f"ErrorHandler initialization failed: {e}")

    # --- 7. Initialize Telegram bot interface ---
    try:
        bot = TelegramBot(
            token=cfg.telegram.token,
            get_response=enhanced.get_response
        )
    except Exception as e:
        sys.exit(f"TelegramBot initialization failed: {e}")

    # --- 8. CLI fallback or Bot ---
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("Shan-D Superadvanced CLI: Type your message or 'exit' to quit.")
        while True:
            try:
                user_input = input("> ")
            except EOFError:
                print("\nExiting CLI.")
                break

            if user_input.lower() in ("exit", "quit"):
                break

            try:
                advanced_security_scan(user_input)
            except Exception as e:
                print(f"Security scan warning: {e}")

            try:
                response = enhanced.get_response(user_input)
            except Exception as e:
                tb = traceback.format_exc()
                response = error_handler.handle_errors(e, context=user_input)
                print(f"[Error handled]\n{tb}")

            try:
                user_db.save_interaction(user_input, response)
            except Exception as e:
                print(f"Warning: Failed to save interaction: {e}")
            try:
                analytics._update_metrics(user_input, response)
            except Exception as e:
                print(f"Warning: Analytics update failed: {e}")

            print(response)
    else:
        try:
            bot.start_polling()
        except Exception as e:
            tb = traceback.format_exc()
            sys.exit(f"Telegram bot polling failed:\n{tb}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Fatal error in main(): {e}\n{tb}")
        sys.exit(1)

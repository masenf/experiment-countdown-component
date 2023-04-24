import pynecone as pc

config = pc.Config(
    app_name="experiment_countdown_component",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    frontend_packages=["react-countdown"],
)

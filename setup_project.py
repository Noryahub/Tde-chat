import os

PROJECT_STRUCTURE = {
    "backend": {
        "__files__": [
            "__init__.py",
            "run.py",
            "requirements.txt"
        ],

        "app": {
            "__files__": [
                "__init__.py"
            ],

            "routes": {
                "__files__": [
                    "__init__.py",
                    "chat_routes.py",
                    "auth_routes.py",
                ]
            },

            "services": {
                "__files__": [
                    "__init__.py",
                    "chatbot_service.py",
                    "orientation_service.py",
                    "user_service.py",
                    "conversation_service.py",
                ]
            },
            "rag":{
                "__files__": [
                    "__init__.py",
                    "scraper.py",
                    "indexer.py",
                    "retriever.py",
                ]
            },
            "validation": {
                "__files__": [
                    "__init__.py",
                    "response_validator.py"
                ]
            },
            "llm":{
                "__files__": [
                    "__init__.py",
                    "groq_client.py",
                    "prompt_builder.py"
                ]
            },

            "models": {
                "__files__": [
                    "__init__.py",
                    "model_loader.py"
                ]
            },

            "nlp": {
                "__files__": [
                    "__init__.py",
                    "preprocess.py"
                ]
            },

            "dialogue": {
                "__files__": [
                    "__init__.py",
                    "dialogue_manager.py"
                ]
            },

            "responses": {
                "__files__": [
                    "__init__.py",
                    "response_generator.py"
                ]
            },

            "database": {
                "__files__": [
                    "__init__.py",
                    "db.py",
                    "models.py"
                ]
            },

            "config": {
                "__files__": [
                    "__init__.py",
                    "config.py"
                ]
            },

            "security": {
                "__files__": [
                    "__init__.py",
                    "security.py"
                ]
            },
        },
    },

    "model": {
        "__files__": [
            "__init__.py"
        ],

        "training": {
            "__files__": [
                "__init__.py",
                "train_model.py",
                "retrain_model.py",
                "intent_model_training.ipynb"
            ]
        },

        "inference": {
            "__files__": [
                "__init__.py",
                "predict.py"
            ]
        },

        "saved_model": {
            "__files__": [
                "intent_model.pkl"
            ]
        },
    },

    "data": {
        "__files__": [
            "__init__.py",
            "dataset.json"
        ],

        "raw": {
            "__files__": []
        },

        "processed": {
            "__files__": []
        },
    },
    "memory": {
        "__files__": [
            "__init__.py",
            "conversation_memory.py"
        ]},


    "frontend": {
        "app": {
            "__files__": [
                "layout.tsx",
                "page.tsx",
                "globals.css"
            ],

            "login": {
                "__files__": ["page.tsx"]
            },

            "register": {
                "__files__": ["page.tsx"]
            },

            "chat": {
                "__files__": ["page.tsx"]
            },

            "profile": {
                "__files__": ["page.tsx"]
            },

            "dashboard": {
                "__files__": ["page.tsx"]
            },

            "analytics": {
                "__files__": ["page.tsx"]
            },

            "users": {
                "__files__": ["page.tsx"]
            },

            "settings": {
                "__files__": ["page.tsx"]
            },

            "signalements": {
                "__files__": ["page.tsx"]
            }
        },

        "components": {

            "layout": {
                "__files__": [
                    "admin-sidebar.tsx",
                    "user-sidebar.tsx",

                    "sidebar-desktop.tsx",
                    "sidebar-mobile.tsx",

                    "sidebar-button.tsx",
                    "sidebar-button-sheet.tsx",

                    "profile-drawer.tsx",

                    "dashboard-layout.tsx",
                    "user-layout.tsx",

                    "top-navbar.tsx"
                ]
            },

            "chat": {
                "__files__": [
                    "chat-header.tsx",
                    "chat-messages.tsx",
                    "chat-input.tsx",
                    "message-bubble.tsx"
                ]
            },

            "auth": {
                "__files__": [
                    "login-form.tsx",
                    "register-form.tsx"
                ]
            },

            "dashboard": {
                "__files__": [
                    "stats-card.tsx",
                    "charts.tsx",
                    "recent-activity.tsx"
                ]
            }
        },

        "providers": {
            "__files__": [
                "auth-provider.tsx"
            ]
        },

        "hooks": {
            "__files__": [
                "use-auth.ts",
                "use-role.ts"
            ]
        },

        "types": {
            "__files__": [
                "auth.ts"
            ]
        },

        "lib": {
            "__files__": [
                "api.ts",
                "auth.ts",
                "utils.ts"
            ]
        }
    },



    "tests": {
        "__files__": [
            "__init__.py",
            "test_api.py",
            "test_model.py"
        ]
    },

    "docs": {
        "__files__": [
            "architecture.md"
        ]
    },

    ".github": {
        "workflows": {
            "__files__": [
                "ci.yml"
            ]
        },
    },

    "migrations": {
        "__files__": [
            "__init__.py",
            "init_db.sql"
        ]
    },

    "__files__": [
        ".env",
        ".gitignore",
        "wsgi.py",
        "README.md"
    ],
}
def create_structure(base_path, structure):
    for name, content in structure.items():

        #fichiers racine
        if name == "__files__":
            for file in content:
                file_path = os.path.join(base_path, file)
                open(file_path, "a").close()
                print(f"✔ Fichier créé : {file_path}")
            continue

        path = os.path.join(base_path, name)

        #créer dossier
        os.makedirs(path, exist_ok=True)
        print(f"Dossier créé : {path}")

        #contenu dossier
        if isinstance(content, dict):
            create_structure(path, content)

        elif isinstance(content, list):
            for file in content:
                file_path = os.path.join(path, file)
                open(file_path, "a").close()
                print(f"✔ Fichier créé : {file_path}")


if __name__ == "__main__":
    base_directory = os.getcwd()
    create_structure(base_directory, PROJECT_STRUCTURE)

    print("\n✅ Structure du projet créée avec succès !")
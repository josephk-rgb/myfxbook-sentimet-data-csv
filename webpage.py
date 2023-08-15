from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'output.csv'

@app.route('/')
def status():
    try:
        # Read the CSV file and count the number of entries
        df = pd.read_csv(CSV_FILE)
        num_entries = len(df)
        status_message = f"Script is running successfully. Number of entries in CSV: {num_entries}"
        status_color = "green"
    except Exception as e:
        status_message = f"Failed to read the CSV file. Error: {e}"
        status_color = "red"

    # Render the status message on a stylish webpage

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Status</title>
        <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
        <style>
            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }

            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% {
                    transform: translateY(0);
                }
                40% {
                    transform: translateY(-15px);
                }
                60% {
                    transform: translateY(-10px);
                }
            }

            body {
                font-family: 'Lato', sans-serif;
                background: linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d);
                color: #eaeaea;
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .status-box {
                animation: fadeIn 1s ease-out;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
                text-align: center;
            }

            .status-icon {
                animation: bounce 5s ease infinite;
                font-size: 3em;
                margin-bottom: 20px;
            }

            .status-message {
                font-weight: 700;
                font-size: 1.5em;
                margin-top: 20px;
                color: {{ status_color }}; /* Color based on the status */
            }

            .entries-message {
                font-weight: 700;
                font-size: 1.5em;
                margin-top: 20px;
            }

            h1 {
                margin: 0;
                font-weight: 700;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="status-box">
            <h1>Status</h1>
            <i class="{{ icon_class }} status-icon"></i>
            <p class="status-message">{{ status_message }}</p>
            <p class="entries-message">{{ entries_message }}</p>
        </div>
    </body>
    </html>
    """,
    status_message="Script is running successfully." if status_color == "green" else "Failed to read the CSV file.",
    entries_message=f"Number of entries in CSV: {num_entries}" if status_color == "green" else f"Error: {status_message}",
    icon_class="fas fa-check-circle" if status_color == "green" else "fas fa-exclamation-circle",
    status_color="green" if status_color == "green" else "red"  
    )





if __name__ == '__main__':
    app.run(debug=True)

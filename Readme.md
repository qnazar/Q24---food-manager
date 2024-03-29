# Q24

Q24 is a web application built with Flask that enables users to easily track the expiration dates of their products. It also includes additional functionality for generating shopping lists and calculating kcal values. The app was developed using Docker and features Celery and Redis for efficient handling of async tasks.

## Features

- Expiration date tracking: Users can easily keep track of the expiration dates for various products and receive timely reminders before items go bad.
- Shopping list generation: The app generates shopping lists based on the user's current inventory, simplifying their shopping process.
- Kcal calculation: Users can easily calculate the kcal values of their meals, enabling them to make more informed decisions about their food choices.

## Technologies Used

- Flask
- Docker
- Celery
- Redis

## Installation

To install Q24, follow these steps:

1. Clone the repository: `git clone https://github.com/qnazar/Q24---food-manager`
2. Start the app: `docker-compose up --build`
3. Go to `127.0.0.1:5010`
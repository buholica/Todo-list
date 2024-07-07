## TODO LIST

Todo List offers an intuitive web-based solution to effortlessly manage personal tasks directly from the browser. Streamlining the workflow, it provides a seamless way to organize, prioritize, and monitor the to-dos with ease and efficiency.
## Features

* The List empowers users with essential task management capabilities, including the ability to seamlessly add and remove tasks, while also facilitating the transition of tasks from active to completed status. 
* Users can conveniently filter tasks based on their status, whether active, completed, or view all tasks at once. 
* Data is saved in Google Sheets through the [SHEETY API](https://sheety.co/) integration, ensuring easy access and management of tasks across devices.
* Each user has a personalized experience with data saved locally in the browser using Flask session, allowing them to see only their relevant tasks.

## Technologies Used
* **Flask**: Handles the logic of the application.
* **Bootstrap**: Provides the design framework for an aesthetically pleasing user interface.
* **Jinja**: Facilitates dynamic templating for seamless integration of backend and frontend components.
* **SHEETY API**: Integrates with Google Sheets for task storage and management.
* **Flask Session**: Saves data locally in the browser to personalize the user experience.
* **Playwright**: Used for browser automation testing.
* **pytest**: A testing framework used to create and run test cases.

## Environment Variables
To run this project, you will need to add the following environment variables to your .env file
* `SHEETY_TOKEN` (token for SHEETY API)
* `DOC_ID` (ID for Google Sheets document where the data is saved)

## Running Tests
To run tests and get an updated report on the testing, run the following command:

```bash
  pytest --template=html1/index.html --report=test_suits/report.html
```

## Additional Information

I utilized the ['Todo List' Bootstrap](https://www.bootdey.com/snippets/view/bs4-todo-list) template as the foundation for this project, but I also incorporated several custom modifications throughout the development process.

⚠️ I am currently creating tests for this web app, so the data is saved in the data.json file because the monthly quota for the Sheety API has expired.
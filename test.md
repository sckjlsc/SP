## Full Stack Engineer

### Background

In most modern web apps, we'll frequently require our users to upload files (i.e. photos).

We can choose to handle this in the web app itself (receiving the files from browser, resizing in the server, uploading to S3 etc)
or we can move it out of the web app and use a standalone file server (i.e. paid service from Cloudinary.com or Filepicker.com).

### Your Task

Write a file server that plays the role of such a standalone file server, like Cloudinary.com or Filepicker.com.

The file server should be able to handle:

- Uploading of the binary file by HTTP `POST` or `PUT`
- Downloading (or viewing) of the binary file by HTTP `GET`

Optionally, the file server may be able to:

- Resize the image dynamically when given desired dimensions, e.g. `128x128`
- Put the uploaded file in a cloud storage service, like S3, for long-term storage

Please write sufficient documentation for us to run an instance of your server and test run the APIs.

### Constraints

#### Time

7 days from XXXX. Please feel free to submit your work any time, before the deadline.

Please timebox yourself to a maximum of 8 hours for this activity.

#### Technology

You are required to use [Go](https://golang.org/).

#### Testing

Please approach this exercise as you would in your day-to-day development workflow.

If you write tests in your daily work, we would love to see them in this exercise too.

#### Git and Commit History

Sync your app to GitHub and allow access to `winston` and `miccheng`.

Please maintain a descriptive and clear Git commit history as it would allow us to better understand your thought process.

### Follow Up

In the event that you are selected for the next round of interview (onsite chat),
please be expected to discuss your work further with us during the interview.

Looking forward to seeing your code!

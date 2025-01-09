# Intelligent Assignment Web Service

## Overview

The Intelligent Assignment Web Service is a Flask-based web application designed to build teams for peer review sites. It uses clustering (k-means) and top trading cycles algorithms to group users and optimize team compositions based on their preferences and collaboration histories. This webservice requires an input of each users ranks [1 being most preferred and 0 indicating no preference] and unique id (pid), as well as the max team size.

## Features

1. **Team Creation (`/merge_teams`)**
   - Uses K-means clustering to group users with similar topic interests.
   - Eliminates competition for any single topic and increases the likelihood that each user obtains their most preferred topic.

2. **Team Member Swapping (`/swap_team_members`)**
   - Uses Top Trading Cycles to swap members who have already worked with members on their team.
   - Maximizes collaboration opportunities by minimizing repetition of team members.
   - Begins by first sorting the list of available members by distance from the teams centroid and then by whether or not other members of the team have worked with them.
   - This method requires a history of users that each user has worked with, along with the general information.

---

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- `virtualenv` (optional, for local development)

### Steps to Install Locally

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd IntelligentAssignment2
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   cd app
   python app.py
   ```
   The service will be available at `http://127.0.0.1:5000/`.

---

## Running with Docker

1. **Build the Docker Image:**
   ```bash
   docker build -t intelligent-assignment .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 5000:5000 intelligent-assignment
   ```

The service will be available at `http://127.0.0.1:5000/`.

---

## Usage

### 1. Creating Teams (`/merge_teams`)

- **Endpoint:** `POST /merge_teams`

- **Input:**
  ```json
  {"users":[{"ranks":[1,0,2,3],"pid":1023},{"ranks":[1,2,0,3],"pid":4535},{"ranks":[0,2,3,1],"pid":1363},{"ranks":[2,1,0,3],"pid":9841}],"max_team_size":4}
  ```

- **Output:**
  ```json
  {"users":[{"ranks":[1,0,2,3],"pid":1023},{"ranks":[1,2,0,3],"pid":4535},{"ranks":[0,2,3,1],"pid":1363},{"ranks":[2,1,0,3],"pid":9841}],"max_team_size":4}
  ```

### 2. Swapping Team Members (`/swap_team_members`)

- **Endpoint:** `POST /swap_team_members`

- **Input:**
  ```json
  {"users":[{"ranks":[1,0,2,3],"history":[4535,9841,9843],"pid":1023},{"ranks":[1,2,0,3],"history":[1023,9843,8542],"pid":4535},{"ranks":[0,2,3,1],"history":[3649,9841,9843],"pid":1363},{"ranks":[2,1,0,3],"history":[1363,1023,3649],"pid":9841}],"teams":[[1023,2549],[4535,9843],[1363,1867,3649],[9841,8542,7521]]}
  ```

- **Output:**
  ```json
  {"users":[{"ranks":[1,0,2,3],"pid":1023,"history":[4535,9841,9843]},{"ranks":[1,2,0,3],"pid":4535,"history":[1023,9843,8542]},{"ranks":[0,2,3,1],"pid":1363,"history":[3649,9841,9843]},{"ranks":[2,1,0,3],"pid":9841,"history":[1363,1023,3649]}],"teams":[[9841,4535],[1023,1363]]}
  ```

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.
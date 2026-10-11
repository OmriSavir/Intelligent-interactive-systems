# Smart Apartment Finder: An AI-Powered Rental Search System

Final project for the **Intelligent Interactive Systems** course.
**Team:** Omri Savir, Marina Kletselman, Tomer Hod

An interactive rental-apartment recommendation system. Users enter their preferences, mark which ones are deal-breakers and rate how much the rest matter. The system then shows matching apartments **one at a time** and learns from each "like" or "dislike" to improve the next recommendation.

## Demo video

[![Watch the demo video](https://img.youtube.com/vi/RAc3zXxaFok/hqdefault.jpg)](https://www.youtube.com/watch?v=RAc3zXxaFok)

*Click the image to watch the demo on YouTube.*

---

## The problem

Searching for a rental apartment is long and frustrating:

- Renters have to weigh **many features** at once: location, price, size, number of rooms, safe room (mamad), parking, pets allowed, accessibility and more.
- They often need to **compromise**, because no single apartment meets every requirement.
- Existing listing sites only offer **hard filters**. These can't tell a must-have from a nice-to-have, so renters either miss good apartments or have to scroll through many irrelevant ones.

Our system replaces plain filtering with an AI-based approach. It separates hard constraints from soft preferences, ranks apartments by how well they match, and adapts to the user's feedback as they browse.

## The interface

The app is built with **Streamlit**. Its interface is in **Hebrew**, with a right-to-left layout.

The system design has three screens. The prototype in this repository implements the renter's side, which is screens 2 and 3.

### 1. Apartment listing

Landlords fill in the apartment's details: location, price, size, number of rooms and binary features such as balcony, safe room and pets allowed. They can also add photos. The apartment then becomes available to potential renters.

### 2. Apartment search

The renter fills in a preference form in three steps. The form is split into steps to reduce cognitive load:

1. **Basic details:** city and neighborhood, ranges for rooms and price, and desired features (balcony, safe room, storage, elevator, accessibility, A/C, private house, pets, parking, sea view, renovated, window bars).
2. **Deal-breakers:** for city, neighborhood, number of rooms and price, the user marks whether the criterion is a deal-breaker. If it isn't, they rate its importance from 1 to 10.
3. **Feature importance:** an importance rating from 1 to 10 for each selected feature.

### 3. Browsing and feedback

Apartments are shown **one at a time**, in a card-swiping style familiar from dating apps:

- Each apartment shows a main photo, its location, number of rooms, price, floor and size.
- A **"More details"** button reveals the full feature list.
- The user marks each apartment as **Liked** or **Disliked**, and the next apartment appears.
- Each recommendation comes with a short **explanation** of why it was shown (see the algorithm section below).

## Recommendation algorithm

### Hard and soft constraints

- **Deal-breakers** are applied as hard filters: apartments that don't meet them are never shown. City and neighborhood are always treated as hard filters.
- All other criteria are **soft preferences**. An apartment that misses a soft preference can still be recommended, but it receives a lower score.

### Importance-weighted similarity

- Every apartment is represented as a binary vector: does it have each feature, and are its rooms and price within the user's range?
- The user's preferences are encoded the same way.
- To reflect importance, each entry is **repeated according to its importance rating (1–10)** in both vectors. A feature rated 10 counts ten times more than a feature rated 1.
- The match is measured with **cosine similarity**, and then scaled from [−1, 1] to [0, 1].

### Cold start: the first five apartments

Before any feedback is available, the apartments are ranked by similarity alone. They are stored in a **priority queue**, and the best match is shown next.

### Learning from feedback

After the user has rated five apartments, the system trains a **logistic regression** model on those ratings. The model estimates the probability that the user will like each remaining apartment. Its features are floor, size, one-hot encoded rooms and price, and the binary features.

The final score of an apartment at step *t* combines both signals:

$$
\text{score}(t) = \frac{5}{2(t-1)} \cdot \text{sim} + \left(1 - \frac{5}{2(t-1)}\right) \cdot \text{reg}
$$

Here, *sim* is the scaled similarity score and *reg* is the probability estimated by the regression model.

- At *t* = 6, the two components have equal weight (0.5 each).
- As *t* grows, the system relies more on what the user actually liked and less on the form.
- After each rating, the scores are recalculated and the queue is reordered.

### Explaining the recommendation

Each recommendation shows the reason it was chosen, based on which component dominated its score:

- *"Based on the preferences and importance levels you entered, here is an apartment you might like"*: the similarity score dominated.
- *"Based on the apartments you liked, you might also like the next one"*: the regression score dominated.

## Human-AI interaction guidelines

The design follows four guidelines for human-AI interaction:

| Guideline | How it is applied |
|---|---|
| **Match relevant social norms** | Apartments are browsed one at a time with like/dislike feedback, similar to familiar matching apps. This makes the system easy to learn. |
| **Reduce cognitive load** | The preference form is split into steps, only one apartment is shown at a time, and extra details are hidden behind a "More details" button. |
| **Remember recent interactions** | The system remembers every rating in the session and uses it for the next recommendations. Apartments that were already rated are not shown again. |
| **Learn from user behavior** | Each like or dislike updates the model immediately and changes which apartment is shown next. |

## User testing

The prototype was tested with **7 users**. Overall they found the system friendly and the instructions clear, and most described a positive experience. Two pieces of feedback stood out:

- Several users found the preference form **long and tiring**.
- Some users expected the process to **end once they found an apartment they liked**, which the prototype doesn't do.

## Future work

- **User interface:** a mobile and tablet version, a more polished design, and reviews of apartments, landlords and neighborhoods from previous tenants.
- **Algorithm:** soft filtering by city and neighborhood, based on distances between areas, and using apartment photos as an input to the recommendations.
- **Language model:** let users describe the apartment they want in free text and fill in the preference form automatically. This could also work as a chatbot that asks follow-up questions.

## Repository contents

```
site.py                                            # Streamlit app: interface + recommendation algorithm
apartments.csv                                     # apartment data used by the app
prototype_intellegent_interactive_systems.ipynb    # Colab notebook for running the app
```

## How to run

Both options require `site.py` and `apartments.csv` from this repository.

### Option 1: run locally

1. Download or clone this repository.
2. Install the dependencies:
   ```bash
   pip install streamlit pandas numpy scikit-learn
   ```
3. From the repository folder, start the app:
   ```bash
   streamlit run site.py
   ```
4. The app opens in your browser at `http://localhost:8501`.

### Option 2: run in Google Colab

1. Open the [Colab notebook](https://colab.research.google.com/drive/10MQHM3gMuc7owdMq3EyDZONuDtOYL3eg?usp=sharing), or create a new notebook.
2. Upload `site.py` and `apartments.csv` to the notebook's files panel. Keep the exact same file names.
3. Run the following code:
   ```
   ! pip install streamlit -q
   !wget -q -O - ipv4.icanhazip.com
   ! streamlit run site.py & npx localtunnel --port 8501
   ```
4. The output shows a **password**, which is the IP address printed on the first line (four numbers separated by dots), and a **URL**.
5. Open the URL, enter the password and click **"Click to Submit"**.
6. Keep the cell running for as long as you use the app.

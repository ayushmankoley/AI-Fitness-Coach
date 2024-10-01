const apiUrl = "http://localhost:8000"; 

const bodyTypes = {
    "Ectomorph": "Ectomorph",
    "Mesomorph": "Mesomorph",
    "Endomorph": "Endomorph"
};

const activityLevels = {
    "Sedentary": "Sedentary",
    "Light": "Light",
    "Moderate": "Moderate",
    "Active": "Active",
    "Athlete": "Athlete"
};

document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const page = this.getAttribute('data-page');
        showPage(page);
    });
});

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
    document.querySelectorAll('nav a').forEach(link => link.classList.remove('active'));
    document.querySelector(`nav a[data-page="${pageId}"]`).classList.add('active');
}

showPage('nutrition');

document.getElementById('signupForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const name = document.getElementById('signupName').value;
    const age = document.getElementById('signupAge').value;
    const height_cm = document.getElementById('signupHeight').value;
    const weight_kg = document.getElementById('signupWeight').value;
    const body_type = document.getElementById('signupBodyType').value;
    const activity_level = document.getElementById('signupActivityLevel').value;

    const signupData = {
        name: name,
        age: parseInt(age),
        height_cm: parseFloat(height_cm),
        weight_kg: parseFloat(weight_kg),
        body_type: bodyTypes[body_type],
        activity_level: activityLevels[activity_level]
    };

    console.log('Sending signup request:', signupData);

    try {
        const response = await fetch(`${apiUrl}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupData),
        });

        console.log('Received signup response:', response);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Signup failed:', response.status, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        console.log('Signup response data:', data);

        if (data && data.id) {
            console.log('User ID received:', data.id);
            alert(`Signup successful! Your user ID is: ${data.id}`);
            showPage('nutrition');
        } else {
            console.error('Incomplete data received in signup response:', data);
            alert('Signup successful, but response data is incomplete.');
        }
    } catch (error) {
        console.error('Error during signup:', error);
        alert(`There was an error during signup: ${error.message}`);
    }
});

document.getElementById('workoutForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const user_id = document.getElementById('user_id').value;

    console.log('Sending workout plan generation request for user_id:', user_id);

    try {
        const response = await fetch(`${apiUrl}/generate_workout/${user_id}`, {
            method: 'GET',
        });

        console.log('Received workout plan response:', response);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Workout plan generation failed:', response.status, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        console.log('Workout plan data:', data);

        if (data && data.workout_plan) {
            const formattedPlan = data.workout_plan
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/###/g, '<hr>');
            
            document.getElementById('workoutPlan').innerHTML = formattedPlan;
        } else {
            console.error('Unexpected response format:', data);
            document.getElementById('workoutPlan').textContent = 'Received an unexpected response format. Please try again.';
        }
    } catch (error) {
        console.error('Error generating workout plan:', error);
        alert(`Failed to generate workout plan: ${error.message}`);
        document.getElementById('workoutPlan').textContent = `Error: ${error.message}`;
    }
});

document.getElementById('nutritionForm').addEventListener('submit', async function (event) {
    event.preventDefault(); 
    
    const user_id = document.getElementById('user_id_nutrition').value;

    console.log('Sending nutrition plan generation request for user_id:', user_id);

    try {
        const response = await fetch(`${apiUrl}/generate_nutrition_plan/${user_id}`, {
            method: 'GET',
        });

        console.log('Received nutrition plan response:', response);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Nutrition plan generation failed:', response.status, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        console.log('Nutrition plan data:', data);

        if (data && data.nutrition_plan) {
            const formattedPlan = data.nutrition_plan
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/###/g, '<hr>');
            
            document.getElementById('nutritionPlan').innerHTML = formattedPlan;
        } else {
            console.error('Unexpected response format:', data);
            document.getElementById('nutritionPlan').textContent = 'Received an unexpected response format. Please try again.';
        }
    } catch (error) {
        console.error('Error generating nutrition plan:', error);
        alert(`Failed to generate nutrition plan: ${error.message}`);
        document.getElementById('nutritionPlan').textContent = `Error: ${error.message}`;
    }
});

document.getElementById('logWorkoutForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const date = document.getElementById('workout_date').value;
    const calories_burned = document.getElementById('calories_burned').value;
    const user_id = document.getElementById('workout_user_id').value;
    const logData = {
        user_id: parseInt(user_id),
        date: date,
        calories_burned: parseFloat(calories_burned),
    };

    console.log('Sending workout log request:', logData);

    try {
        const response = await fetch(`${apiUrl}/log_workout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(logData),
        });

        console.log('Received workout log response:', response);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Workout logging failed:', response.status, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();
        console.log('Workout log data:', data);

        alert('Workout logged successfully!');
    } catch (error) {
        console.error('Error logging workout:', error);
        alert(`Failed to log workout: ${error.message}`);
    }
});

window.addEventListener('load', () => showPage('nutrition'));
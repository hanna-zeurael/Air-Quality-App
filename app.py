import streamlit as st
import requests
from geopy.geocoders import Nominatim
from streamlit_js_eval import streamlit_js_eval

#function to get user's city based on IP or location
def get_user_city():
    try:
        response = request.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.jason()
            return data.get("city", "unknown city")
    except:
        return "unknown city"
   #function to send browser notification 
def send_browser_notification(message):
    streamlit_js_eval(
        js_expressions=f"alert('{message}')",
        key="notification"
    )
   
#streamlit app UI
st.title("🌍 Air Quality Prediction & Alert System")

st.sidebar.header("Select Location")
city = st.sidebar.text_input("Enter City Name", "Addis Ababa")

#Button to fetch air quality data
if st.sidebar.button("Get My Location"):
    city = get_user_city()  # Detect location and set it as city
    st.sidebar.success(f"Detected City: {city}")

if st.sidebar.button("Get Air Quality Data"):
     if not city:
        st.sidebar.error("⚠ Please enter a city or use 'Get My Location' button.")
     else:
         api_url = f"http://127.0.0.1:5000/air_quality?city={city}"  # Update with your Flask API URL
         response = requests.get(api_url)#to enter the url

         if response.status_code == 200:
           data = response.json()
         st.subheader(f"Air Quality in {city}")
         st.write(f"PM2.5 Level: {data['pm25']} µg/m³")
         st.write(f"PM10 Level: {data['pm10']} µg/m³")
         st.write(f"NO2 Level: {data['no2']} µg/m³")
         st.write(f"Temperature: {data['temperature']} °C")
         st.write(f"Humidity: {data['humidity']}%")
        
        # Alert System and Notification
     if data['pm25'] > 50:
            st.warning("High Pollution Alert! Limit outdoor activities.")
            send_browser_notification(f"PM2.5 is {data['pm25']} µg/m³! Stay indoors if possible!")
     elif data['pm10'] > 100:
      st.warning("High PM10 Pollution Alert! Limit outdoor activities.")
      send_browser_notification(f"PM10 is {data['pm10']} µg/m³! Becareful!")
     elif data['no2'] > 200:
      st.warning("High NO2 Pollution Alert! Limit outdoor activities.")
      send_browser_notification(f" NO2 is {data['no2']} µg/m³! Avoid polluted areas!")
      if data['temperature'] > 35:
        st.warning(" High Temperature Alert! Stay hydrated and avoid direct sunlight.")
        send_browser_notification(f" Temperature is {data['temperature']}°C! Stay cool!")

     elif data['temperature'] < 5:
       st.warning("❄ Low Temperature Alert! Dress warmly.")
       send_browser_notification(f"❄ Temperature is {data['temperature']}°C! Stay warm!")

     if data['humidity'] > 80:
       st.warning("High Humidity Alert! Risk of discomfort and mold growth.")
       send_browser_notification(f"Humidity is {data['humidity']}%! Be cautious.")

     elif data['humidity'] < 30:
      st.warning("Low Humidity Alert! Risk of dry skin and throat irritation.")
      send_browser_notification(f"Humidity is {data['humidity']}%! Use a humidifier if needed.")
     else:
            st.success("✅ Air quality is good.")
else:
        st.error("Error fetching data. Please check the API.")


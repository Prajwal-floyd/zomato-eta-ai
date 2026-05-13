import {
  FaTrafficLight,
  FaClock,
  FaChartLine,
  FaBrain
} from "react-icons/fa"

import { motion } from "framer-motion"

import { useState } from "react"

function App() {

  const [loading, setLoading] = useState(false)

  const [eta, setEta] = useState("--")

  const [traffic, setTraffic] = useState("Medium")

  const [weather, setWeather] = useState("Sunny")

  const [distance, setDistance] = useState(8)

  const [orderHour, setOrderHour] = useState(20)

  const trafficMap = {

    Low: 1,
    Medium: 2,
    High: 3

  }

  const weatherMap = {

    Sunny: 1,
    Rainy: 2,
    Fog: 3

  }

  const predictETA = async () => {

    setLoading(true)

    try {

      const response = await fetch(

        "http://127.0.0.1:8000/predict",

        {

          method: "POST",

          headers: {

            "Content-Type": "application/json"

          },

          body: JSON.stringify({

            distance_km:
              Number(distance),

            traffic_score:
              trafficMap[traffic],

            weather_score:
              weatherMap[weather],

            is_rush_hour:
              (
                orderHour >= 18 &&
                orderHour <= 22
              )
                ? 1
                : 0,

            prep_time: 15,

            is_weekend: 0,

            city_avg_eta: 30

          })

        }

      )

      const data = await response.json()

      console.log(data)

      setEta(data.predicted_eta)

    }

    catch (error) {

      console.log(error)

      alert("Prediction failed")

    }

    finally {

      setLoading(false)

    }

  }

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      {/* NAVBAR */}

      <nav className="flex items-center justify-between px-10 py-6 border-b border-slate-800">

        <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">

          Zomato ETA AI

        </h1>

        <p className="text-slate-400">

          Logistics Intelligence Dashboard

        </p>

      </nav>


      {/* HERO */}

      <motion.section

        initial={{ opacity: 0, y: 40 }}

        animate={{ opacity: 1, y: 0 }}

        transition={{ duration: 1 }}

        className="px-10 py-20"

      >

        <h2 className="text-7xl md:text-8xl font-bold leading-tight bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">

          AI-Powered <br />

          Delivery ETA Prediction

        </h2>

        <p className="mt-6 text-slate-400 text-xl max-w-2xl leading-9">

          Predict delivery estimates using traffic,
          weather, and operational intelligence.

        </p>

      </motion.section>


      {/* METRICS */}

      <section className="px-10 pb-20">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">


          {/* ETA */}

          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <div className="flex items-center gap-3 text-slate-400 text-lg">

              <FaClock className="text-cyan-400" />

              <p>Predicted ETA</p>

            </div>

            <h3 className="text-6xl font-bold mt-4">

              {eta}

              <span className="text-2xl ml-2">

                mins

              </span>

            </h3>

            <p className="mt-6 text-green-400">

              Live AI prediction output

            </p>

          </motion.div>


          {/* TRAFFIC */}

          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <div className="flex items-center gap-3 text-slate-400 text-lg">

              <FaTrafficLight className="text-red-400" />

              <p>Traffic Impact</p>

            </div>

            <h3 className="text-5xl font-bold mt-4 text-red-400">

              {traffic.toUpperCase()}

            </h3>

            <p className="mt-6 text-slate-400">

              Real-time congestion monitoring

            </p>

          </motion.div>


          {/* CONFIDENCE */}

          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <div className="flex items-center gap-3 text-slate-400 text-lg">

              <FaChartLine className="text-cyan-400" />

              <p>Prediction Confidence</p>

            </div>

            <h3 className="text-5xl font-bold mt-4 text-cyan-400">

              92%

            </h3>

            <p className="mt-6 text-slate-400">

              High prediction reliability

            </p>

          </motion.div>

        </div>

      </section>


      {/* INPUT PANEL */}

      <section className="px-10 pb-20">

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-10 shadow-2xl">

          <h2 className="text-3xl font-bold mb-10 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">

            Live ETA Prediction

          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">


            <select

              value={traffic}

              onChange={(e) =>
                setTraffic(e.target.value)
              }

              className="bg-slate-800 border border-slate-700 rounded-xl p-4 outline-none"

            >

              <option>Low</option>
              <option>Medium</option>
              <option>High</option>

            </select>


            <select

              value={weather}

              onChange={(e) =>
                setWeather(e.target.value)
              }

              className="bg-slate-800 border border-slate-700 rounded-xl p-4 outline-none"

            >

              <option>Sunny</option>
              <option>Rainy</option>
              <option>Fog</option>

            </select>


            <input

              type="number"

              value={distance}

              onChange={(e) =>
                setDistance(e.target.value)
              }

              placeholder="Distance"

              className="bg-slate-800 border border-slate-700 rounded-xl p-4 outline-none"

            />


            <input

              type="number"

              value={orderHour}

              onChange={(e) =>
                setOrderHour(
                  Number(e.target.value)
                )
              }

              placeholder="Order Hour"

              className="bg-slate-800 border border-slate-700 rounded-xl p-4 outline-none"

            />

          </div>


          <button

            onClick={predictETA}

            className="mt-10 bg-gradient-to-r from-cyan-400 to-blue-500 hover:scale-105 transition-all duration-300 text-black font-bold px-8 py-4 rounded-2xl shadow-2xl"

          >

            {

              loading

                ? "AI Analyzing Route..."

                : "Predict ETA"

            }

          </button>

        </div>

      </section>


      {/* INSIGHTS */}

      <section className="px-10 pb-20">

        <div className="flex items-center gap-4 mb-10">

          <FaBrain className="text-cyan-400 text-4xl" />

          <h2 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">

            AI Operational Insights

          </h2>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">


          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <h3 className="text-xl font-bold text-cyan-400">

              Traffic Analysis

            </h3>

            <p className="mt-4 text-slate-400 leading-7">

              Heavy congestion significantly
              increases ETA predictions.

            </p>

          </motion.div>


          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <h3 className="text-xl font-bold text-green-400">

              Delivery Efficiency

            </h3>

            <p className="mt-4 text-slate-400 leading-7">

              Route efficiency remains stable
              despite urban congestion.

            </p>

          </motion.div>


          <motion.div

            whileHover={{ scale: 1.03 }}

            className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl"

          >

            <h3 className="text-xl font-bold text-red-400">

              Rush Hour Impact

            </h3>

            <p className="mt-4 text-slate-400 leading-7">

              Peak-hour delivery conditions
              amplify ETA variability.

            </p>

          </motion.div>

        </div>

      </section>

    </div>

  )
}

export default App
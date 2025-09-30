import { use, useEffect, useState } from "react";
import { Stats } from "./api";

export default function Dashboard() {

  // React states for the dashboard
  const [popularBooks, setPopularBooks] = useState([]);
  const [popularAuthors, setPopularAuthors] = useState([]);
  const [userTotal, setUserTotal] = useState(null);
  const [userTopAuthors, setUserTopAuthors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    // mounted variable will be used as a flag to prevent updates if the components unmounts mid request
    let mounted = true;

    (async () => {
      setLoading(true);
      setErr("");
      
      try {
      // Get all the request in parallel and wait for them all to come back (or for one to throw an error)
      const [pb, pa, ut, uta] = await Promise.all([
        Stats.popularBooks(10),
        Stats.popularAuthors(10),
        Stats.userTotal(),
        Stats.userTopAuthors(3)
      ]);

      // Avoid setting the state if unmounted
      if (!mounted){
        return;
      }

      // Set the states with the data we just retrieved
      setPopularBooks(pb)
      setPopularAuthors(pa)
      setUserTotal(ut)
      setUserTopAuthors(uta)

    }
    catch (e) {
      if (!mounted) {
        return;
      }
      // Error message
      setErr(e.message || "Failed to load data")
    }
    finally {
      if (mounted) {
        // Finished loading the data
        setLoading(false);
        }
      }
    })
  })
}
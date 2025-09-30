import { useEffect, useState } from "react";
import { Stats } from "./api";

export default function Dashboard() {

  // React states for the dashboard
  const [popularBooks, setPopularBooks] = useState([]);
  const [popularAuthors, setPopularAuthors] = useState([]);
  const [userTotal, setUserTotal] = useState(null);
  const [userTopAuthors, setUserTopAuthors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

}
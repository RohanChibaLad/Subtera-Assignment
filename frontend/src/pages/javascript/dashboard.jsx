import { use, useEffect, useState } from "react";
import { Stats } from "./api";

export default function Dashboard() {

  // ----- Javascript ----- \\

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
          setLoading(false);
        }
      }
    })();

    // Cleanup runs on unmount
    return () => { mounted = false; };
  }, []); 

// First item in popularAuthors is the most popular
  const mostPopularAuthor = popularAuthors[0] || null;

  // ----- HTML Components ----- \\

  return (
    <div className="page">
      <header className="nav">
        <div className="title">Library Dashboard</div>
      </header>

      <main className="container">
        {err && <div className="card error">{err}</div>}
        
        <section classname="grid">
          <div className="card">
            <h3 className="card-title"> Most Popular Author</h3>
            {loading ? ("Loading..."): mostPopularAuthor ? (
              <>
              <div className="big">{mostPopularAuthor.author_name}</div>
              <div className="muted">{mostPopularAuthor.total_readers} total readers</div>
              </>
            ) : (
              <div className="muted">No data</div>
            )}
          </div>

          <div className="card">
            <h3 className="card-title">Your Total Books:</h3>
            {loading ? ("Loading..."): userTotal ? (
              <>
                <div className="big">{userTotal.total_books}</div>
                <div className="muted">{userTotal.reader_name}</div>
              </>
            ) : (
              <div className="muted">No user</div>
            )}
          </div>

          <div className="card">
            <h3 className="card-title">Your Top 3 Authors</h3>
            {loading ? ("Loading…") : userTopAuthors.length ? (
              <ol className="list">
                {userTopAuthors.map((a) => (
                  <li key={a.author_id}>
                    <span>{a.author_name}</span>
                    <span className="pill">{a.books_read}</span>
                  </li>
                ))}
              </ol>
            ) : (
              <div className="muted">No data</div>
            )}
          </div>
        </section>

        <section className="card">
          <h3 className="card-title">Most Popular Books</h3>
          {loading ? ("Loading…") : popularBooks.length ? (
            <table className="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Title</th>
                  <th>Author</th>
                  <th>Readers</th>
                </tr>
              </thead>
              <tbody>
                {popularBooks.map((b, i) => (
                  <tr key={b.book_id}>
                    <td>{i + 1}</td>
                    <td>{b.title}</td>
                    <td>{b.author_name}</td>
                    <td>{b.readers_counter}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="muted">No books found</div>
          )}

        </section>
      </main>
    </div>
  )


}
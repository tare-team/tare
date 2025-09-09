import { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: '{ hello }' })
    })
      .then(res => res.json())
      .then(result => setMessage(result.data.hello))
      .catch(() => setMessage('Error'));
  }, []);

  return <div>{message}</div>;
}

export default App;

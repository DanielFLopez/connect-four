import React, {useState, useRef, useEffect} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import './App.css';
import axios from 'axios'

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        height: 50,
        width: 50,
        "&:hover": {
            background: "#efefef"
        }
    },
    one: {
        background: "#c50606"
    },
    two: {
        background: "#62c506"
    },
    control: {
        padding: theme.spacing(1),
    },
    body: {
        marginTop: 100
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
    winner: {
        fontFamily: "Staatliches",
        color: "#000",
        fontSize: "-webkit-xxx-large"
    }
}));

function App() {
    const [matrix, setMatrix] = useState([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]);
    const [name, setName] = useState('')
    const [text, setText] = useState('')
    const [game, setGame] = useState(0)
    const [turn, setTurn] = useState('')
    const [winner, setWinner] = useState('')
    const [status, setStatus] = useState(false)
    const [type, setType] = useState(0)
    const classes = useStyles();


    const webSocket = useRef(null);
    useEffect(() => {
        webSocket.current = new WebSocket("ws://0.0.0.0:8000/ws/game");
        webSocket.current.onopen = (message) => {
            console.log("Conected")
        };
        webSocket.current.onmessage = (message) => {
            const data = JSON.parse(message.data);
            if(data.type_message === 'message'){
                setMatrix(data.matrix_value)
                setTurn(data.turn)
            }else if(data.type_message === 'winner'){
                console.log("winner")
                console.log(data)
                setWinner(data.message)
            }else if(data.type_message === 'initial'){
                console.log(data)
                setTurn(data.turn)
                setStatus(data.status)
            }
        };
        webSocket.current.onclose = (message) => {
            console.log(message)
            console.log("Bye")
        };
        return () => webSocket.current.close();
    }, []);

    const one = {
        backgroundColor: '#c50606'
    }

    const two = {
        backgroundColor: '#03a001'
    }

    const handleClick = (e) => {
        e.preventDefault();
        if (name === turn && status){
            if (e.target.dataset.status === "0") {
                let row = e.target.dataset.row
                let column = e.target.dataset.column
                let data = {'column': column, 'row': row, 'status': e.target.dataset.status, 'user': name, 'game': game, 'type_message': 'message', 'type_game': type}
                webSocket.current.send(JSON.stringify(data))
            }
        }else{
            alert("Is not your turn")
        }
    }

    const getLabel = (value) => {
        if (value === 0) {
            return {}
        } else if (value === 1) {
            return one
        } else if (value === 2) {
            return two
        }
    }

    const handleChange = (e) => {
        setText(e.target.value);
    }

    const handlePvp = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/game/register/', {
            user: text,
            type_game: 1
        })
        .then(function (response) {
            console.log("register")
            console.log(response.data)
            setName(text);
            setGame(response.data.game_id)
            webSocket.current.send(JSON.stringify({'game': response.data.game_id, 'type_message': 'initial'}))
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    const handlePve = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/game/register/', {
            user: text,
            type_game: 2
        })
        .then(function (response) {
            console.log("register")
            console.log(response.data)
            setName(text);
            setGame(response.data.game_id)
            setType(response.data.type_game)
            webSocket.current.send(JSON.stringify({'game': response.data.game_id, 'type_message': 'initial'}))
        })
        .catch(function (error) {
            console.log(error);
        });
    }


    const handleClose = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/game/close/')
        .then(function (response) {
            console.log(response.data.message)
            setMatrix([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
            setName('')
            setTurn('')
            setWinner('')
            setText('')
            setStatus(false)
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    return (
        <div className="App">
            {name ? (<AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" className={classes.title}>
                        Player {name} {turn ? ( <div>it's the turn of {turn} </div>):(<div> Waiting turn...</div>)}
                    </Typography>
                    <Button color="inherit" onClick={handleClose}>Close game</Button>
                </Toolbar>
            </AppBar>) : (<form onSubmit={handlePvp}>
                <TextField required id="standard-required" label="Type your name" onChange={handleChange} value={text}/>
                <Button onClick={handlePvp}>PVP</Button>
                <Button onClick={handlePve}>PVE</Button>
            </form>)
            }
            {name ? (<div className={classes.body}>
                <Grid container className={classes.root} spacing={1}>
                    <Grid item xs={12}>
                        {matrix.map((row, indexRow) => (
                            <Grid container justify="center" spacing={1} key={indexRow}>
                                {row.map((value, indexColumn) => (
                                    <Grid item key={indexColumn}>
                                        <Paper className={classes.paper} style={getLabel(value)} onClick={handleClick}
                                               data-status={value} data-row={indexRow} data-column={indexColumn}/>
                                    </Grid>)
                                )}
                            </Grid>
                        ))}
                    </Grid>
                </Grid>
            </div>

            ): (
                <div> Waiting...</div>
            )}
            <div className={classes.winner}> {winner}</div>
        </div>
    );
}

export default App;

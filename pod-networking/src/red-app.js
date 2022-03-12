const express = require('express')

const PORT = 8080
const POD_IP = process.env.POD_IP
const NODE_NAME = process.env.NODE_NAME
const NAMESPACE = process.env.NAMESPACE

const app = express()

app.get('/red', (req, res) => {
    res.render('red', {podIp: POD_IP, nodeName: NODE_NAME, namespace: NAMESPACE})
})

app.get('/hello', (req, res) => {
    res.json("Hello I'm Red.")
})

app.listen(PORT, () => {
    console.log(`Server is runnign on ${PORT}`)
})
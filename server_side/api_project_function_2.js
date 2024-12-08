// api_project_function_2.js
const OpenAI = require("openai");
require('dotenv').config();

const openai = new OpenAI();

exports.get_trivia = async (req, res) => {
  try {
    const randomNumber = Math.floor(Math.random() * 1000);
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { "role": "user", "content": `Give me a unique trivia question that can be answered in one word. ${randomNumber}` }
      ]
    });

    const question = completion.choices[0].message.content.trim();

    res.status(200).json({
      "message": "success",
      "question": question
    });
  } catch (err) {
    console.log("**Error in /trivia");
    console.log(err.message);

    res.status(500).json({
      "message": err.message,
      "question": ""
    });
  }
};

exports.check_answer = async (req, res) => {
  try {
    const { question, user_answer } = req.body;

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { "role": "user", "content": `What is the one-word answer to the trivia question: "${question}"? Provide just the word without any punctuation.` }
      ]
    });

    const correct_answer = completion.choices[0].message.content.trim().toLowerCase();

    const result = (user_answer === correct_answer);

    res.status(200).json({
      "message": "success",
      "correct_answer": correct_answer,
      "result": result
    });
  } catch (err) {
    console.log("**Error in /trivia/answer");
    console.log(err.message);

    res.status(500).json({
      "message": err.message,
      "correct_answer": "",
      "result": false
    });
  }
};
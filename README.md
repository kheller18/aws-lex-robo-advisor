# AWS Lex Robo Advisor

![license badge](https://shields.io/badge/license-GNU-blue)


## Description

This project uses AWS Lex and Lambda. I created a Lex Bot that will give recommendations to a user based on their inputs. The Lex Bot uses Lambda to check against constraints.

The general criteria for the bot is seen below:
  + Bot name: RoboAdvisor
  + Language: English (US)
  + Output voice: Salli
  + Session timeout: 5 Minutes
  + Sentiment analysis: No
  + COPPA: No
  + Advanced Options: No
  + All other options: Default values

Our intents are defined below:
  + Utterances
    + I want to save money for my retirement
    + I'm {age} and I would like to invest for my retirement
    + I'm ​{age} and I want to invest for my retirement
    + I want the best option to invest for my retirement
    + I'm worried about my retirement
    + I want to invest for my retirement
    + I would like to invest for my retirement

  + Slots
    + firstName (AMAZON.US_FIRST_NAME)
    + age (AMAZON.NUMBER)
    + investmentAmount (AMAZON.NUMBER)
    + riskLevel (AMAZON.AlphaNumeric)

Once everything has been defined, we can test our bot using only Lex. The GIF is seen below:

![Lex Gif](Videos/robo_advisor_gif_v1.gif)

Now that we've seen that the bot works, we have to use Lambda to control our constraints. The constraints are as follows:
  + 0 >= age <=65
  + investmentAmount >= 5000

With the Lamda function tested and complete, we integrate it into Lex. We can see the new Lex GIF below:

![Lex Lambda Gif](Videos/robo_advisor_lambda_gif.gif)

## Table of Contents

- [AWS Lex Robo Advisor](#aws-lex-robo-advisor)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [1. Installation](#1-installation)
  - [2. Usage](#2-usage)
  - [3. License](#3-license)
  - [4. Contributing](#4-contributing)
  - [5. Tests](#5-tests)
  - [6. Deployment](#6-deployment)
  - [7. Contact](#7-contact)


## 1. Installation

  If you would like to clone the repository, type "git clone https://github.com/kheller18/aws-lex-robo-advisor.git".


## 2. Usage

  After cloning the repository locally, you'll need to have the packages listed in [Installation](#1-installation) installed on your machine.


## 3. License

	MIT License

  Copyright (c) 2023 Keenan Heller

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.


## 4. Contributing

  + [Keenan Heller](https://github.com/kheller18)


## 5. Tests

  + There are four tests associated with this repository. They can be found in the "Test_Events" directory.
    + ageError
    + correctDialog
    + incorrectAmountError
    + negativeAgeError


## 6. Deployment

  + There is currently no live deployment of this notebook on a common server, but it can be configured using AWS Lex and Lambda.


## 7. Contact

  + [Keenan's LinkedIn](https://www.linkedin.com/in/keenanheller/)
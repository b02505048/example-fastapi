#!/bin/bash

. ./activate

uvicorn app.main:server --reload
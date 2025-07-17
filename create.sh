#!/bin/bash

for i in {1..20}; do
    curl -X POST -H "Content-Type: application/json" -d "{\"nom\": \"prof$i\", \"email\": \"prof$i@example.com\"}" http://localhost:8000/api/professionnels/
done

for i in {1..20}; do
    curl -X POST -H "Content-Type: application/json" -d "{\"nom\": \"admin$i\", \"email\": \"admin$i@example.com\"}" http://localhost:8000/api/administrateurs/
done
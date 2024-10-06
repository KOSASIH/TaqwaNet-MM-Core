package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/grpc"

	pb "github.com/taqwanet/muamalah-matrix/muamalah-matrix-api"
)

func main() {
	// Create a new gRPC client
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	// Create a new MuamalahMatrix client
	client := pb.NewMuamalahMatrixClient(conn)

	// Create a new request
	req := &pb.MuamalahMatrixRequest{
		UserId: "user123",
		Amount: 100,
	}

	// Call the MuamalahMatrix method
	resp, err := client.MuamalahMatrix(context.Background(), req)
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	// Print the response
	fmt.Println(resp.GetMessage())
}

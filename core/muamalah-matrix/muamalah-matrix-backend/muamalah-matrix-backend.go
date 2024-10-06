package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/grpc"

	pb "github.com/taqwanet/muamalah-matrix/muamalah-matrix-backend"
)

func main() {
	// Create a new gRPC server
	srv := grpc.NewServer()

	// Register the MuamalahMatrix service
	pb.RegisterMuamalahMatrixServer(srv, &muamalahMatrixServer{})

	// Start the server
	log.Println("Starting server on port 50051")
	if err := srv.Serve(listener); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

type muamalahMatrixServer struct{}

func (s *muamalahMatrixServer) MuamalahMatrix(ctx context.Context, req *pb.MuamalahMatrixRequest) (*pb.MuamalahMatrixResponse, error) {
	// Implement the MuamalahMatrix logic here
	return &pb.MuamalahMatrixResponse{Message: "Hello, " + req.UserId}, nil
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name_prefix = "metricflow-rds-"
  vpc_id      = aws_vpc.metricflow_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.metricflow_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "metricflow-rds-sg"
    Environment = var.environment
  }
}

# DB Subnet Group
resource "aws_db_subnet_group" "metricflow_db_subnet_group" {
  name       = "metricflow-db-subnet-group"
  subnet_ids = aws_subnet.private_subnets[*].id

  tags = {
    Name        = "metricflow-db-subnet-group"
    Environment = var.environment
  }
}

# Route Table for Public Subnets
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.metricflow_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.metricflow_igw.id
  }

  tags = {
    Name        = "metricflow-public-rt"
    Environment = var.environment
  }
}

# Route Table Association for Public Subnets
resource "aws_route_table_association" "public_rta" {
  count          = length(aws_subnet.public_subnets)
  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# NAT Gateway for Private Subnets
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  depends_on = [aws_internet_gateway.metricflow_igw]

  tags = {
    Name        = "metricflow-nat-eip"
    Environment = var.environment
  }
}

resource "aws_nat_gateway" "metricflow_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnets[0].id

  tags = {
    Name        = "metricflow-nat"
    Environment = var.environment
  }
}

# Route Table for Private Subnets
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.metricflow_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.metricflow_nat.id
  }

  tags = {
    Name        = "metricflow-private-rt"
    Environment = var.environment
  }
}

# Route Table Association for Private Subnets
resource "aws_route_table_association" "private_rta" {
  count          = length(aws_subnet.private_subnets)
  subnet_id      = aws_subnet.private_subnets[count.index].id
  route_table_id = aws_route_table.private_rt.id
}
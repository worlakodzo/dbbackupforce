resource "aws_vpc" "self" {
  cidr_block       = var.vpc_cidr 
  instance_tenancy = var.instance_tenancy
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = var.tags
  }
}

resource "aws_internet_gateway" "self" {
  vpc_id = aws_vpc.self.id

  tags = {
    Name = var.tags
  }
}

data "aws_availability_zones" "available" {
}


resource "random_shuffle" "az_list" {
  input        = data.aws_availability_zones.available.names
  result_count = 2
}

resource "aws_subnet" "public" {
  count                   = var.public_sn_count
  vpc_id                  = aws_vpc.self.id
  cidr_block              = var.public_cidrs[count.index]
  availability_zone       = random_shuffle.az_list.result[count.index]
  map_public_ip_on_launch = var.map_public_ip_on_launch
  tags = {
    Name = "${var.tags}-public-${count.index}"
  }
}

resource "aws_subnet" "private" {
  count                   = var.private_sn_count
  vpc_id                  = aws_vpc.self.id
  cidr_block              = var.private_cidrs[count.index]
  availability_zone       = random_shuffle.az_list.result[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.tags}-private-${count.index}"
  }
}


# Use default route table as public route
resource "aws_default_route_table" "public" {
  default_route_table_id = aws_vpc.self.default_route_table_id

  route {
    cidr_block = var.rt_route_cidr_block
    gateway_id = aws_internet_gateway.self.id
  }

  tags = {
    Name = var.tags
  }
  
}

resource "aws_route_table_association" "public" {
  count          = var.public_sn_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_default_route_table.public.id
}


# NAT Elastic IP
resource "aws_eip" "self" {
  vpc = true

  tags = {
    Name = "worlako-portfolio-ngw-ip"
  }
}

# NAT Gateway
resource "aws_nat_gateway" "self" {
  allocation_id = aws_eip.self.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "worlako-portfolio-ngw"
  }

  depends_on = [aws_internet_gateway.self]
}


# Creating a Route Table for the Nat Gateway!
resource "aws_route_table" "private" {
  depends_on = [aws_nat_gateway.self]

  vpc_id = aws_vpc.self.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.self.id
  }

  tags = {
    Name = "worlako-portfolio-ngw-rt"
  }

}

# Creating an Route Table Association of the NAT Gateway route 
# table with the Private Subnet!
resource "aws_route_table_association" "private" {
  depends_on = [aws_route_table.private]

  subnet_id      = aws_subnet.private[0].id
  route_table_id = aws_route_table.private.id
}
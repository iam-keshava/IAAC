resource "aws_instance" "ec2_instance" {
  count = var.instance_count

  ami           = "ami-0287a05f0ef0e9d9a" # Amazon Linux 2 AMI, replace with your preferred AMI
  instance_type = "t2.micro"

  tags = {
    Name = "instance-${count.index + 1}"
  }
}

output "public_ips" {
  value = aws_instance.ec2_instance[*].public_ip
}

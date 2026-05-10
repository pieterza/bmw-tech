# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = var.cluster_name
  kubernetes_version = var.cluster_version

  enable_cluster_creator_admin_permissions = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets


  # EKS Addons
  addons = {
    coredns = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy = {}
    vpc-cni = {
      before_compute = true
    }
  }

  self_managed_node_groups = {
    bmw_runners = {
      instance_type = "t3.medium"


      min_size     = 2
      max_size     = 2
      desired_size = 2

    }
  }

}


# ECR pull access
resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  role       = module.eks.self_managed_node_groups["bmw_runners"].iam_role_name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

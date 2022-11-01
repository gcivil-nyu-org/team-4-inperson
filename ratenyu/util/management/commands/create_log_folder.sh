echo "creating logs folder"
{
    mkdir -p ../../../../logs
    echo > ../../../../logs/django.log
} || {
    echo "failed to create logs folder"
    exit 1
}
echo "logs folder created"
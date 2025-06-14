# 🚀 Deploy VirtualTA Knowledge Base on Render

## Prerequisites
- GitHub account
- Render account (free at render.com)
- Your API key for the embedding service

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - VirtualTA Knowledge Base"
   git branch -M main
   git remote add origin https://github.com/yourusername/virtualta-project.git
   git push -u origin main
   ```

2. **Make sure these files are in your repo**:
   - ✅ `app.py` (your main FastAPI application)
   - ✅ `knowledge_base.db` (your database file)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `static/` folder (web interface)
   - ✅ `render.yaml` (Render configuration)
   - ✅ `start_render.py` (production startup script)

### Step 2: Deploy to Render

1. **Go to Render Dashboard**:
   - Visit https://render.com
   - Sign up or log in
   - Click "New +" → "Web Service"

2. **Connect Your Repository**:
   - Choose "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select your VirtualTA repository

3. **Configure Your Service**:
   ```
   Name: virtualta-knowledge-base
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python start_render.py
   ```

4. **Set Environment Variables**:
   ```
   API_KEY = your_actual_api_key_here
   PORT = 10000
   ```

5. **Configure Advanced Settings**:
   - Instance Type: Free tier (512MB RAM) or Starter ($7/month, 512MB RAM)
   - Auto-Deploy: Yes (recommended)

6. **Deploy**:
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)

### Step 3: Verify Deployment

Once deployed, your service will be available at: `https://your-service-name.onrender.com`

**Test your deployment**:

1. **Health Check**:
   ```bash
   curl https://your-service-name.onrender.com/health
   ```

2. **Web Interface**:
   Visit `https://your-service-name.onrender.com` in your browser

3. **API Documentation**:
   Visit `https://your-service-name.onrender.com/docs`

4. **Test API Call**:
   ```bash
   curl -X POST "https://your-service-name.onrender.com/query" \
        -H "Content-Type: application/json" \
        -d '{"question": "What is machine learning?"}'
   ```

### Step 4: Custom Domain (Optional)

1. **In Render Dashboard**:
   - Go to your service → Settings → Custom Domains
   - Add your domain (e.g., `api.yourdomain.com`)
   - Update your DNS records as instructed

## 🔧 Configuration Options

### Environment Variables
Set these in Render Dashboard → Settings → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `API_KEY` | `your_api_key` | **Required** - Your embedding service API key |
| `PORT` | `10000` | Port for the application (Render sets automatically) |

### Instance Types

| Plan | RAM | CPU | Storage | Price | Best For |
|------|-----|-----|---------|-------|----------|
| Free | 512MB | 0.1 CPU | 1GB | $0/month | Testing, demos |
| Starter | 512MB | 0.5 CPU | 20GB | $7/month | Small projects |
| Standard | 2GB | 1 CPU | 100GB | $25/month | Production |

**Recommendation**: Start with **Free tier** for testing, upgrade to **Starter** for production use.

## 📊 Monitoring Your Deployment

### Built-in Monitoring
Render provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, response times
- **Health Checks**: Automatic monitoring
- **Alerts**: Email notifications for issues

### Custom Health Monitoring
Use the included health check script:
```bash
python health_check.py https://your-service-name.onrender.com
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails - Dependencies**:
   ```
   Solution: Check requirements.txt formatting
   Make sure all packages are valid
   ```

2. **Service Won't Start**:
   ```
   Check logs for:
   - Port binding issues
   - Missing environment variables
   - Database file permissions
   ```

3. **API Key Errors**:
   ```
   Verify API_KEY environment variable is set
   Check if key needs "Bearer " prefix
   ```

4. **Database Not Found**:
   ```
   Ensure knowledge_base.db is in your Git repository
   Check file size (should be ~96MB)
   ```

5. **High Memory Usage**:
   ```
   Consider upgrading to Starter plan
   SQLite + embeddings can use 400-500MB RAM
   ```

### Getting Help

1. **Check Render Logs**:
   - Dashboard → Your Service → Logs
   - Look for error messages during startup

2. **Test Locally First**:
   ```bash
   python start_render.py
   # Should work locally before deploying
   ```

3. **Render Support**:
   - Community forum: community.render.com
   - Documentation: render.com/docs

## 🔄 Updating Your Deployment

### Automatic Updates
- Push to your main branch
- Render automatically rebuilds and deploys
- Zero-downtime deployments

### Manual Updates
1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically detects changes
4. New version deployed automatically

## 🔐 Security Best Practices

1. **Environment Variables**:
   - Never commit API keys to Git
   - Use Render's environment variable settings

2. **HTTPS**:
   - Render provides free SSL certificates
   - All traffic is encrypted by default

3. **Access Control**:
   - Consider adding rate limiting
   - Monitor API usage in logs

## 💰 Cost Optimization

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- 750 hours/month of usage
- Slower cold starts

### Paid Tier Benefits
- Always-on service
- Faster performance
- More memory/CPU
- Priority support

## 🎯 Performance Tips

1. **Database Optimization**:
   - Your SQLite file works great for read-heavy workloads
   - Consider PostgreSQL for write-heavy scenarios

2. **Caching**:
   - Embeddings are cached in database
   - Consider Redis for additional caching

3. **Monitoring**:
   - Watch memory usage
   - Monitor response times
   - Set up alerts for issues

## 📞 Support

- **Render Documentation**: https://render.com/docs
- **Community**: https://community.render.com
- **Status Page**: https://status.render.com

## 🎉 Success Checklist

- ✅ Repository pushed to GitHub
- ✅ Render service created and deployed
- ✅ Environment variables configured
- ✅ Health check passes
- ✅ API responds to test queries
- ✅ Web interface accessible
- ✅ Custom domain configured (optional)

**Your VirtualTA Knowledge Base is now live and accessible to the world! 🌍** 
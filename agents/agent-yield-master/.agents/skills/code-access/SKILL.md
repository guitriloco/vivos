---
name: Code Access
description: Git repository access — clone, commit, push, and create pull requests
---

# Code Access

Git credentials are pre-configured on the sandbox. You can clone and work with the team's repositories immediately.

Check `/home/team/shared/WORKFLOW.md` for the team's code delivery process (e.g., branching strategy, PR expectations, merge policy). Follow that workflow when completing code tasks.

## Your Workspace

- Your home directory (`~`) is your private workspace — other team members cannot access it
- Each team member clones and works on their own copy of the repository
- To share files with teammates, copy them to `/home/team/shared/`

## Git Workflow

1. Clone a repository into your home directory: `git clone https://github.com/owner/repo.git ~/project`
2. `cd ~/project`
3. **Read project instructions**: Check for `CLAUDE.md` or `AGENTS.md` in the project root (`cat CLAUDE.md AGENTS.md 2>/dev/null`). These files contain project-specific conventions, coding standards, and workflow rules — follow them strictly throughout your work.
4. Create a working branch: `git checkout -b feature/description`
5. Explore the codebase and understand the task
6. Make changes using file tools and bash
7. Test your changes (build, lint, test as appropriate)
8. Stage and commit: `git add -A && git commit -m "descriptive message"`
9. Before pushing, call `get_git_credentials` to refresh authentication (tokens expire hourly)
10. Push: `git push -u origin branch-name`
11. Create a pull request if the workflow calls for it: `gh pr create --title "..." --body "..."`
12. When calling `finish_task`, include any PR URLs via the `pr_urls` parameter

## Tips

- Use `gh` CLI for GitHub operations (PRs, issues, repo info)
- You can work on multiple repositories simultaneously
- Always refresh credentials before push operations
- Follow existing code patterns and conventions in the repository
- Keep commits atomic and well-described

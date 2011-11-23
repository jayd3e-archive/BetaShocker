<%inherit file="layouts/base.mako"/>

<%def name="body()">
	<h2>STATS</h2>
	<table class="stats_table" cellpadding="0" cellspacing="0">
		<tr>
			<th>Average Total Posts</th>
			<td>${avg_total_posts}</td>
		</tr>
		<tr>
			<th>Average Days of Membership</th>
			<td>${avg_days}</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ <font color="red">300+</font> posts</th>
			<td>${perc_old_300}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ between <font color="red">20</font> and <font color="red">300</font> posts</th>
			<td>${perc_old_20}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">RANDOM</font> people</th>
			<td>${perc_random}%</td>
		</tr>
	</table>
</%def>

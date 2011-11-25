<%inherit file="layouts/base.mako"/>

<%def name="body()">
	<h2>WINNER STATS</h2>
	<table class="stats_table" cellpadding="0" cellspacing="0">
		<tr>
			<th>Average Total Posts</th>
			<td>${winner_avg_total_posts}</td>
		</tr>
		<tr>
			<th>Average Days of Membership</th>
			<td>${winner_avg_days}</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ <font color="red">300+</font> posts</th>
			<td>${winner_perc_old_300}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ between <font color="red">20</font> and <font color="red">300</font> posts</th>
			<td>${winner_perc_old_20}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">NEW</font> people w/ < <font color="red">20</font> posts</th>
			<td>${winner_perc_random}%</td>
		</tr>
	</table>
	<h2>TOTAL ENTRANT STATS</h2>
	<table class="stats_table" cellpadding="0" cellspacing="0">
		<tr>
			<th>Average Total Posts</th>
			<td>${entrant_avg_total_posts}</td>
		</tr>
		<tr>
			<th>Average Days of Membership</th>
			<td>${entrant_avg_days}</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ <font color="red">300+</font> posts</th>
			<td>${entrant_perc_old_300}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">OLD</font> members w/ between <font color="red">20</font> and <font color="red">300</font> posts</th>
			<td>${entrant_perc_old_20}%</td>
		</tr>
		<tr>
			<th>% of <font color="red">NEW</font> people w/ < <font color="red">20</font> posts</th>
			<td>${entrant_perc_random}%</td>
		</tr>
	</table>
	<div class="note"><font color="red">*Note:</font> An old member is defined as over a year old from join date, and a new member is defined as less than a year old.</div>
</%def>

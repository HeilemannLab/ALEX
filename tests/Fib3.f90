C file: FIB1.F90
      subroutine FIB(i, j, t1, t2, f1, f2, t, check)
C
C     Compare values, if t1 is greater than t2, t2 gets written
C	  to t, j increases 1, i stays the same. In every other case,
C	  if t2 is greater than t1 OR if t1==t2, t1 gets written to t.
C
	  implicit none
C
      integer i, j, t, check, t1, t2, f1, f2
	  intent(in) t1, t2, f1, f2
	  intent(inout) i, j
	  intent(out) t, check
C		
	  if (t1.gt.t2) then
        t=t2
        j=j+1
      else
        t=t1
        i=i+1
	  endif
	  check=1
	  if ((i.eq.f1).or.(j.eq.f2)) then
        check=0
	  endif
      end subroutine
C end file FIB1.F90
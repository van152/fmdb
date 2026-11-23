__int64 *__fastcall sub_14412D630(__int64 *a1)
{
  __int64 v2; // rcx

  if ( a1[2] != 0 )
  {
    v2 = *a1;
    if ( *a1 != 0 )
      (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v2 + 40LL))(a1: v2, a2: a1[1]);
  }
  a1[3] = 0;
  a1[2] = 0;
  a1[1] = 0;
  return a1;
}

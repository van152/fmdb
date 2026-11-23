int *__fastcall sub_143C95D60(__int64 a1, int *a2)
{
  __int64 v4; // rdx
  __int64 v5; // rcx
  int v6; // edx

  v4 = *(_QWORD *)(a1 + 96);
  if ( v4 == 0 )
  {
    v6 = *(_DWORD *)(a1 + 288);
    if ( v6 == *(_DWORD *)(a1 + 292) )
      goto LABEL_9;
LABEL_10:
    *a2 = v6;
    return a2;
  }
  if ( *(_BYTE *)(a1 + 245) == 0 || (v5 = *(_QWORD *)(v4 + 272)) == 0 )
    v5 = *(_QWORD *)(v4 + 264);
  v6 = *(_DWORD *)(a1 + 288);
  if ( v6 != *(_DWORD *)(a1 + 292) )
    goto LABEL_10;
  if ( v5 == 0 )
  {
LABEL_9:
    *a2 = -16777216;
    return a2;
  }
  sub_1411DF450(v5, a2, 0, 3, 1, 1u, 0);
  return a2;
}

char __fastcall sub_14401D500(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rax
  unsigned int v5; // eax
  __int64 v6; // rax
  int v7; // ecx

  v4 = sub_141751B70(a1[3], a1[4], a2);
  if ( v4 == a1[4] || ((v5 = (unsigned int)(v4 - *((_DWORD *)a1 + 6)) >> 3) & 0x80u) != 0 )
  {
    v6 = sub_141751B70(a1[6], a1[7], a2);
    v7 = -1;
    if ( v6 != a1[7] )
      v7 = (unsigned __int64)(v6 - a1[6]) >> 3;
    LOBYTE(v5) = -1;
    if ( (v7 & 0x80u) == 0 )
      return v7 + ((unsigned int)(*((_DWORD *)a1 + 8) - *((_DWORD *)a1 + 6)) >> 3);
  }
  return v5;
}

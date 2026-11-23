char __fastcall sub_143C23BF0(__int64 a1, char a2)
{
  unsigned __int16 v2; // r8
  __int64 v3; // r11
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  bool v7; // zf
  __int64 v8; // rdx
  char result; // al

  v2 = dword_141AAE084 & 0x1FF;
  v3 = *(_QWORD *)(a1 + 256);
  v4 = v3 + 136;
  v5 = 136;
  if ( a2 != 0 )
  {
    v5 = 160;
    v4 = v3 + 160;
  }
  if ( HIWORD(dword_141AAE084) < *(_WORD *)(v4 + 2)
    || HIWORD(dword_141AAE084) <= *(_WORD *)(v4 + 2) && v2 < (unsigned __int16)(*(_WORD *)(v3 + v5) & 0x1FF) )
  {
    return 0;
  }
  v6 = v3 + 140;
  v7 = a2 == 0;
  v8 = 140;
  if ( !v7 )
  {
    v8 = 164;
    v6 = v3 + 164;
  }
  if ( HIWORD(dword_141AAE084) > *(_WORD *)(v6 + 2) )
    return 0;
  result = 1;
  if ( HIWORD(dword_141AAE084) >= *(_WORD *)(v6 + 2) && v2 >= (unsigned __int16)(*(_WORD *)(v3 + v8) & 0x1FF) )
    return 0;
  return result;
}

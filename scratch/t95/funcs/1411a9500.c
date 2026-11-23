// THUNK ALIAS -> sub_143FE3A50 (jmp:0x1411a9500->0x143fe3a50)
bool __fastcall sub_143FE3A50(_QWORD *a1, char a2, char a3)
{
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rdx
  __int64 v8; // rcx

  if ( a3 != 0 && (unsigned __int8)sub_140087070() == 0 )
    return false;
  v5 = a1[10];
  if ( a1[6] == 0 || v5 == 0 || *(_DWORD *)(v5 + 12) != 40 )
  {
    if ( a1[11] != 0 )
      v5 = a1[11];
    if ( v5 == 0 || *(_DWORD *)(v5 + 12) != 40 )
      return false;
  }
  v6 = *(_QWORD *)(v5 + 96);
  if ( v6 == 0 )
    return false;
  if ( *(_BYTE *)(v5 + 245) != 0 && (v7 = *(_QWORD *)(v6 + 272)) != 0 )
  {
    if ( *(char *)(v7 + 1150) < 0 )
      return false;
  }
  else if ( *(char *)(*(_QWORD *)(v6 + 264) + 1150LL) < 0 )
  {
    return false;
  }
  if ( a2 == 0 )
    return true;
  v8 = *(_QWORD *)(v5 + 176);
  return v8 != 0 && sub_1409083C0(v8);
}

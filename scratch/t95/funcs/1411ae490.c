// THUNK ALIAS -> sub_143FF1520 (jmp:0x1411ae490->0x143ff1520)
char __fastcall sub_143FF1520(_QWORD *a1)
{
  __int64 v2; // rax
  __int64 v3; // rdi
  __int64 v4; // rcx
  __int64 v5; // rdx
  __int64 v6; // rcx
  __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rcx
  __int64 v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rcx
  unsigned __int16 v14; // dx
  char result; // al

  if ( (unsigned __int8)sub_140087070() != 0 )
  {
    v2 = a1[6];
    v3 = a1[10];
    if ( v2 != 0 && v3 != 0 )
    {
      v4 = a1[10];
      if ( *(_DWORD *)(v3 + 12) == 40 )
        goto LABEL_9;
    }
    v4 = a1[11];
    if ( v4 == 0 )
      v4 = a1[10];
    if ( v4 != 0 && *(_DWORD *)(v4 + 12) == 40 )
    {
LABEL_9:
      v5 = *(_QWORD *)(v4 + 96);
      if ( v5 != 0 )
      {
        if ( *(_BYTE *)(v4 + 245) != 0 && (v6 = *(_QWORD *)(v5 + 272)) != 0 )
        {
          if ( *(char *)(v6 + 1150) >= 0 )
            goto LABEL_28;
        }
        else if ( *(char *)(*(_QWORD *)(v5 + 264) + 1150LL) >= 0 )
        {
          goto LABEL_28;
        }
      }
    }
  }
  if ( (unsigned __int8)sub_140087070() == 0 )
    return 0;
  v2 = a1[6];
  v3 = a1[10];
  if ( v2 == 0 || v3 == 0 || (v7 = a1[10], *(_DWORD *)(v3 + 12) != 129985) )
  {
    v7 = a1[11];
    if ( v7 == 0 )
      v7 = a1[10];
    if ( v7 == 0 || *(_DWORD *)(v7 + 12) != 129985 )
      return 0;
  }
  v8 = *(_QWORD *)(v7 + 96);
  if ( *(_BYTE *)(v7 + 245) != 0 && (v9 = *(_QWORD *)(v8 + 272)) != 0 )
  {
    if ( *(char *)(v9 + 1150) < 0 )
      return 0;
  }
  else if ( *(char *)(*(_QWORD *)(v8 + 264) + 1150LL) < 0 )
  {
    return 0;
  }
LABEL_28:
  if ( v2 == 0 )
    return 0;
  if ( v3 == 0 )
    return 0;
  v10 = *(_QWORD *)(v3 + 176);
  if ( v10 == 0 )
    return 0;
  if ( !sub_1409083C0(v10) )
    return 0;
  v11 = *(_QWORD *)(v3 + 176);
  if ( v11 == 0 )
    return 0;
  v12 = *(_QWORD *)(v11 + 520);
  if ( v12 == 0 )
    return 0;
  v13 = *(_QWORD *)(v12 + 440);
  if ( v13 == 0 )
    return 0;
  v14 = *(_WORD *)(v11 + 560);
  result = 1;
  if ( v14 > *(_WORD *)(v13 + 4) )
    return 0;
  return result;
}

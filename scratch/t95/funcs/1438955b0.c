__int64 __fastcall sub_1438955B0(__int64 a1)
{
  unsigned int v1; // esi
  int v3; // eax
  __int64 v4; // rcx
  unsigned int v5; // eax
  __int64 v6; // rcx
  __int64 v7; // rcx

  LOBYTE(v1) = 1;
  if ( a1 == 0 )
    return v1;
  v3 = *(_DWORD *)(a1 + 12);
  if ( v3 <= 150918 )
  {
    if ( v3 <= 114552 )
    {
      if ( v3 == 20 || v3 == 104551 || v3 == 108530 )
        return v1;
    }
    else if ( v3 > 150715 )
    {
      if ( v3 == 150716 || v3 == 150785 )
        return v1;
    }
    else if ( (unsigned int)(v3 - 114553) < 2 || v3 == 115064 )
    {
      return v1;
    }
    goto LABEL_31;
  }
  if ( v3 <= 1301431 )
  {
    if ( v3 > 214398 )
    {
      if ( v3 == 214399 || v3 == 1300021 )
        return v1;
    }
    else if ( v3 == 150919 || v3 == 150988 )
    {
      return v1;
    }
    goto LABEL_31;
  }
  if ( v3 <= 100000022 )
  {
    if ( v3 == 1301432 || v3 == 19102111 )
      return v1;
    goto LABEL_31;
  }
  if ( v3 == 2000200284 )
    return v1;
  if ( v3 != 100000023 )
  {
LABEL_31:
    v6 = *(_QWORD *)(a1 + 176);
    if ( v6 == 0 || (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v6 + 328LL))(v6) == 0 )
    {
      if ( *(_BYTE *)(a1 + 244) != 28 )
        return 0;
      v7 = *(_QWORD *)(a1 + 176);
      if ( v7 != 0 && (sub_1409083C0(v7) || *(_QWORD *)(a1 + 176) != 0 && (unsigned __int8)sub_140908A80() != 0) )
        return 0;
    }
    return v1;
  }
  v4 = *(_QWORD *)(a1 + 176);
  if ( v4 != 0 )
  {
    LOBYTE(v5) = sub_1409083C0(v4);
    v1 = v5;
    LOBYTE(v1) = v5 ^ 1;
  }
  return v1;
}

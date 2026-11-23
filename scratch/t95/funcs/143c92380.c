__int64 __fastcall sub_143C92380(__int64 a1)
{
  __int64 v1; // rdi
  _QWORD *v3; // rax
  __int64 v4; // rdx
  __int64 v5; // rcx
  __int64 *v6; // rax
  __int64 *v7; // rdx
  __int64 v8; // rcx
  __int64 v9; // rcx
  __int64 v10; // rax
  __int64 v11; // rdx
  __int64 *v12; // r8
  __int64 *v13; // rdx

  v3 = *(_QWORD **)(a1 + 176);
  if ( v3 == nullptr )
  {
LABEL_41:
    LOBYTE(v1) = *(_QWORD *)(a1 + 168) != 0;
    return (unsigned int)v1;
  }
  v1 = v3[7];
  v4 = v3[8];
  if ( v1 != v4 )
  {
    v5 = v3[7];
    while ( *(_DWORD *)v5 != 1666609219 )
    {
      v5 += 16;
      if ( v5 == v4 )
        goto LABEL_20;
    }
    if ( v5 != v4 && *(_QWORD *)(v5 + 8) != 0 )
    {
      v6 = nullptr;
      while ( *(_DWORD *)v1 != 1666609219 )
      {
        v1 += 16;
        if ( v1 == v4 )
          goto LABEL_16;
      }
      if ( v1 == v4 )
        v6 = nullptr;
      else
        v6 = *(__int64 **)(v1 + 8);
LABEL_16:
      v7 = &qword_141B5A4A0;
      if ( v6 != nullptr )
        v7 = v6;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v7 + 48LL))(*v7) == 0 )
      {
        LODWORD(v1) = 0;
        return (unsigned int)v1;
      }
      v3 = *(_QWORD **)(a1 + 176);
    }
  }
LABEL_20:
  LOBYTE(v1) = 1;
  if ( v3[57] == v3[56] )
  {
    v8 = v3[115];
    if ( v8 == 0 || *(_BYTE *)(v8 + 143) == 0 )
    {
      v9 = v3[7];
      v10 = v3[8];
      if ( v9 == v10 )
        goto LABEL_41;
      v11 = v9;
      while ( *(_DWORD *)v11 != 1666609219 )
      {
        v11 += 16;
        if ( v11 == v10 )
          goto LABEL_41;
      }
      if ( v11 == v10 || *(_QWORD *)(v11 + 8) == 0 )
        goto LABEL_41;
      v12 = nullptr;
      while ( *(_DWORD *)v9 != 1666609219 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_38;
      }
      v12 = v9 == v10 ? nullptr : *(__int64 **)(v9 + 8);
LABEL_38:
      v13 = &qword_141B5A4A0;
      if ( v12 != nullptr )
        v13 = v12;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v13 + 48LL))(*v13) == 0 )
        goto LABEL_41;
    }
  }
  return (unsigned int)v1;
}

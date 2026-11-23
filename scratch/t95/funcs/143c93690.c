__int64 __fastcall sub_143C93690(__int64 a1)
{
  __int64 v1; // rbx
  _QWORD *v3; // rdi
  int v4; // eax
  signed int v5; // ebp
  int v6; // ebp
  unsigned __int8 v7; // si
  int v8; // ecx
  __int64 v9; // rdx
  __int64 v10; // rcx
  __int64 v11; // rdi
  char v12; // al
  __int64 v13; // rax
  __int64 v14; // rax
  unsigned __int64 v15; // rsi
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rdx
  __int64 *v19; // rbp
  __int64 *v20; // rdx

  v3 = *(_QWORD **)(a1 + 176);
  if ( v3 != nullptr && v3[36] == a1 )
  {
    if ( v3[24] != v3[25] )
    {
      v13 = v3[115];
      if ( v13 != 0 )
      {
        if ( *(_BYTE *)(v13 + 143) != 0 )
          goto LABEL_57;
      }
      else
      {
        v14 = v3[56];
        if ( v3[57] != v14 )
        {
          v15 = 0;
          while ( 1 )
          {
            v1 = *(_QWORD *)(v14 + 8 * v15);
            if ( v1 != 0
              && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v1 + 368LL))(v1) != 0
              && (*(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v1 + 368LL))(v1) + 57) & 1) != 0 )
            {
              goto LABEL_57;
            }
            ++v15;
            v14 = v3[56];
            if ( v15 >= (v3[57] - v14) >> 3 )
            {
              v3 = *(_QWORD **)(a1 + 176);
              if ( v3 == nullptr )
                goto LABEL_55;
              break;
            }
          }
        }
      }
      v16 = v3[7];
      v17 = v3[8];
      if ( v16 != v17 )
      {
        v18 = v3[7];
        while ( *(_DWORD *)v18 != 1666609219 )
        {
          v18 += 16;
          if ( v18 == v17 )
            goto LABEL_52;
        }
        if ( v18 != v17 && *(_QWORD *)(v18 + 8) != 0 )
        {
          v19 = nullptr;
          while ( *(_DWORD *)v16 != 1666609219 )
          {
            v16 += 16;
            if ( v16 == v17 )
              goto LABEL_48;
          }
          if ( v16 == v17 )
            v19 = nullptr;
          else
            v19 = *(__int64 **)(v16 + 8);
LABEL_48:
          v20 = &qword_141B5A4A0;
          if ( v19 != nullptr )
            v20 = v19;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v20 + 48LL))(*v20) == 0 )
            goto LABEL_56;
          v3 = *(_QWORD **)(a1 + 176);
        }
      }
LABEL_52:
      if ( v3[57] == v3[56]
        && (unsigned __int8)sub_14099A560(v3) == 0
        && (unsigned __int8)sub_140948740(*(_QWORD *)(a1 + 176)) == 0 )
      {
LABEL_55:
        if ( *(_QWORD *)(a1 + 168) == 0 )
        {
LABEL_56:
          LODWORD(v1) = 0;
          return (unsigned int)v1;
        }
      }
    }
LABEL_57:
    LOBYTE(v1) = 1;
    return (unsigned int)v1;
  }
  v4 = *(_DWORD *)(a1 + 12);
  LOBYTE(v1) = 1;
  if ( ((unsigned int)(v4 - 74) < 0x10 || (unsigned int)(v4 - 215852) <= 1) && v3 != nullptr )
  {
    v5 = ((*((_DWORD *)v3 + 114) - *((_DWORD *)v3 + 112)) & 0xFFFFFFF8) << 21;
    if ( ((*((_DWORD *)v3 + 114) - *((_DWORD *)v3 + 112)) & 0x400) != 0 || v5 == 0 )
    {
      LOBYTE(v1) = 1;
      return (unsigned int)v1;
    }
    v6 = v5 >> 24;
    LOBYTE(v1) = 1;
    v7 = 0;
    while ( 1 )
    {
      if ( (v7 & 0x80u) == 0 )
      {
        v9 = *(_QWORD *)(a1 + 176);
        v10 = *(_QWORD *)(v9 + 448);
        if ( (*(_QWORD *)(v9 + 456) - v10) >> 3 > (unsigned __int64)v7 )
        {
          v11 = *(_QWORD *)(v10 + 8LL * v7);
          if ( v11 != 0
            && ((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v11 + 296LL))(v11) == 0
             || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v11 + 296LL))(v11) == a1) )
          {
            v12 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v11 + 656LL))(v11);
            v8 = 1;
            if ( (v1 & 1) != 0 )
              v8 = (unsigned __int8)v1;
            if ( v12 == 6 )
              v8 = 0;
            LODWORD(v1) = v8;
            if ( (v8 & 1) != 0 )
              break;
          }
        }
      }
      if ( v6 <= (char)++v7 )
        return (unsigned int)v1;
    }
    goto LABEL_57;
  }
  return (unsigned int)v1;
}

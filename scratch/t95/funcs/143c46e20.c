__int64 __fastcall sub_143C46E20(_QWORD *a1)
{
  __int64 v2; // rax
  __int64 v3; // rdx
  unsigned __int64 v4; // rdx
  __int64 v5; // rcx
  unsigned __int8 *v6; // rax
  unsigned int v7; // ebp
  __int64 *v8; // rcx
  __int64 v9; // rax
  unsigned __int64 v10; // rdi
  __int64 *v11; // rcx
  _BYTE *v12; // rbx

  v2 = a1[9];
  v3 = a1[10] - v2;
  if ( v3 != 0 )
  {
    v4 = v3 >> 4;
    v5 = 1;
    if ( v4 >= 2 )
      v5 = v4;
    v6 = (unsigned __int8 *)(v2 + 12);
    while ( *(v6 - 1) != 108 )
    {
      v6 += 16;
      if ( --v5 == 0 )
        goto LABEL_7;
    }
    v7 = *v6;
  }
  else
  {
LABEL_7:
    v7 = 0;
  }
  v8 = (__int64 *)a1[22];
  v9 = *v8;
  if ( v8[1] != *v8 )
  {
    v10 = 0;
    do
    {
      v12 = *(_BYTE **)(v9 + 8 * v10);
      if ( v12 != nullptr && (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v12 + 56LL))(v12) == 24 )
        LOBYTE(v7) = (v12[20] == 0) + v7;
      ++v10;
      v11 = (__int64 *)a1[22];
      v9 = *v11;
    }
    while ( v10 < (v11[1] - *v11) >> 3 );
  }
  return v7;
}

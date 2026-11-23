_BYTE *__fastcall sub_143E30770(_BYTE *a1, unsigned int *a2)
{
  __int64 v4; // rcx
  __int64 *v5; // rax
  __int64 *v6; // rbx
  int v7; // eax
  char v8; // al
  unsigned int v9; // ecx
  __int64 v11; // rdx
  __int64 v12; // rdx

  v4 = qword_141B60C30;
  v5 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v4 != 1986359923 )
    {
      v4 += 16;
      if ( v4 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v4 == qword_141B60C38 )
      v5 = nullptr;
    else
      v5 = *(__int64 **)(v4 + 8);
  }
LABEL_8:
  v6 = &qword_141B5A4A0;
  if ( v5 != nullptr )
    v6 = v5;
  if ( ((*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v6 + 8LL))(*v6, v6) == 0
     || (*(int (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v6 + 64LL))(*v6, v6) <= 3024)
    && ((*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 1
     || (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 2
     || (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 15
     || (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 24
     || (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 25
     || (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2) == 5) )
  {
    v7 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 80LL))(*(_QWORD *)a2, a2);
    *a1 = BYTE2(v7);
    a1[1] = BYTE1(v7);
    a1[2] = v7;
    a1[3] = HIBYTE(v7);
  }
  else
  {
    if ( dword_141B62F80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B62F80);
      if ( dword_141B62F80 == -1 )
      {
        qword_141B62F50 = 0x141759DF8LL;
        byte_141B62F58 = 13;
        LOBYTE(v11) = 13;
        sub_1412EA280(&qword_141B62F60, v11);
        LOBYTE(v12) = 13;
        sub_1412EB230(&qword_141B62F70, v12);
        qword_141B62F50 = 0x14189EA48LL;
        qword_141B62F60 = 0x14189EB28LL;
        qword_141B62F70 = 0x14189EB48LL;
        sub_141751048(sub_1413360A0);
        sub_141750EA0(&dword_141B62F80);
      }
    }
    if ( *(__int64 **)a2 == &qword_141B62F50 )
    {
      v9 = a2[2];
    }
    else
    {
      v8 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a2 + 8LL))(*(_QWORD *)a2, a2);
      v9 = 0;
      if ( v8 == 4 )
        v9 = (unsigned __int8)BYTE2(a2[2]) | ((unsigned __int8)a2[2] << 16) | a2[2] & 0xFF00FF00;
    }
    *(_DWORD *)a1 = v9;
  }
  return a1;
}

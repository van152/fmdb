__int64 __fastcall sub_14153E480(__int64 a1, int a2, unsigned int *a3)
{
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rsi
  int v9; // ecx
  int v10; // eax
  __int64 v11; // rbx
  __int64 v12; // rdi
  int v13; // eax
  int v14; // ecx
  __int64 v15; // rsi
  char v16; // bp
  __int64 v17; // rbp
  __int64 v18; // rcx
  unsigned int v19; // eax
  _DWORD *v20; // rsi
  __int64 v21; // rbp
  int v22; // eax
  int v23; // eax
  __int64 v25; // [rsp+20h] [rbp-38h] BYREF
  int v26; // [rsp+28h] [rbp-30h] BYREF

  LODWORD(v6) = 0;
  v7 = sub_140FE84D0();
  if ( a2 <= 1886151032 )
  {
    v8 = v7;
    if ( a2 == 1668052322 )
    {
      v11 = qword_141B5FDB8;
      sub_140FE7960(&v25, a3, 1130589301);
      v12 = sub_140F7A940(v11, &v25);
      if ( v8 != 0 )
      {
        v13 = *(_DWORD *)(v8 + 12);
        LODWORD(v25) = v13;
        v14 = *(_DWORD *)(v8 + 16);
        if ( v14 == 0 )
          v14 = v13;
      }
      else
      {
        LODWORD(v25) = -1;
        v13 = -1;
        v14 = -1;
      }
      v6 = qword_141B5FDB8;
      HIDWORD(v25) = v14;
      if ( v13 == *(_DWORD *)(a1 + 32) && v14 == *(_DWORD *)(a1 + 36)
        || (v20 = (_DWORD *)(a1 + 32),
            (v21 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                     qword_141B5FDB8,
                     &v25)) == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 32LL))(v6, a1 + 32)) )
      {
        if ( v12 != 0 )
        {
          *(_DWORD *)(a1 + 40) = *(_DWORD *)(v12 + 12);
          v23 = *(_DWORD *)(v12 + 16);
          if ( v23 == 0 )
            v23 = *(_DWORD *)(v12 + 12);
        }
        else
        {
          *(_DWORD *)(a1 + 40) = -1;
          v23 = -1;
        }
        *(_DWORD *)(a1 + 44) = v23;
      }
      else
      {
        if ( v12 != 0 )
        {
          *v20 = *(_DWORD *)(v12 + 12);
          v22 = *(_DWORD *)(v12 + 16);
          if ( v22 == 0 )
            v22 = *(_DWORD *)(v12 + 12);
        }
        else
        {
          *v20 = -1;
          v22 = -1;
        }
        *(_DWORD *)(a1 + 36) = v22;
      }
      goto LABEL_44;
    }
    if ( a2 == 1768124269 )
    {
      if ( v7 != 0 )
      {
        v9 = *(_DWORD *)(v7 + 12);
        LODWORD(v25) = v9;
        v10 = *(_DWORD *)(v7 + 16);
        if ( v10 == 0 )
          v10 = v9;
      }
      else
      {
        LODWORD(v25) = -1;
        v9 = -1;
        v10 = -1;
      }
      v15 = qword_141B5FDB8;
      HIDWORD(v25) = v10;
      if ( v9 != *(_DWORD *)(a1 + 40) || (v16 = 1, v10 != *(_DWORD *)(a1 + 44)) )
      {
        LODWORD(v6) = a1 + 40;
        v17 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(qword_141B5FDB8, &v25);
        v16 = v17 == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v15 + 32LL))(v15, a1 + 40);
      }
      LOBYTE(v6) = 1;
      if ( v16 != (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                    *(_QWORD *)a3,
                    a3) )
      {
        v18 = *(_QWORD *)(a1 + 40);
        *(_QWORD *)(a1 + 40) = *(_QWORD *)(a1 + 32);
        *(_QWORD *)(a1 + 32) = v18;
      }
    }
  }
  else
  {
    switch ( a2 )
    {
      case 2003136100:
        if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5C8D0);
          if ( dword_141B5C8D0 == -1 )
          {
            sub_140DBC9B0(&qword_141B5C8A0);
            sub_141751048(sub_140DBCA10);
            sub_141750EA0(&dword_141B5C8D0);
          }
        }
        if ( *(__int64 **)a3 == &qword_141B5C8A0 )
        {
          v19 = a3[2];
          HIWORD(v26) = v19 >> 17;
          LOWORD(v26) = (v19 >> 8) & 0x1FF | ((_WORD)v19 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, &v25, a3);
          sub_1413CA830(&v26, &v25);
        }
        else
        {
          v26 = 124518401;
        }
        *(_DWORD *)(a1 + 48) = v26;
        goto LABEL_44;
      case 2002872165:
        *(_DWORD *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                 *(_QWORD *)a3,
                                 a3);
        goto LABEL_44;
      case 1886151033:
        sub_140FE7960(&v25, a3, 1348825715);
        *(_QWORD *)(a1 + 24) = v25;
LABEL_44:
        LOBYTE(v6) = 1;
        break;
      default:
        break;
    }
  }
  return (unsigned int)v6;
}

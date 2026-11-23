char __fastcall sub_143FB9190(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  __int64 v6; // rsi
  __int64 v7; // rax
  __int64 v8; // rsi
  __int64 v9; // rax
  int v10; // eax
  __int64 v11; // rbx
  __int64 v12; // rax
  unsigned int v13; // eax
  unsigned int v14; // eax
  int v15; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v16[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 <= 1835103330 )
  {
    switch ( a2 )
    {
      case 1668052322:
        v8 = qword_141B5FDB8;
        sub_140FE7960(v16, a3, 1130589301);
        v9 = sub_140F7A940(v8, v16);
        if ( v9 != 0 )
          v10 = *(_DWORD *)(v9 + 12);
        else
          v10 = -1;
        *(_DWORD *)(a1 + 48) = v10;
        break;
      case 1668246896:
        v11 = qword_141B5FDC0;
        sub_140FE7960(v16, a3, 1668246896);
        v12 = sub_140F7A940(v11, v16);
        if ( v12 != 0 )
          *(_DWORD *)(a1 + 40) = *(_DWORD *)(v12 + 12);
        else
          *(_DWORD *)(a1 + 40) = -1;
        break;
      case 1701733492:
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
        if ( (__int64 *)*a3 == &qword_141B5C8A0 )
        {
          v14 = *((_DWORD *)a3 + 2);
          HIWORD(v15) = v14 >> 17;
          LOWORD(v15) = (v14 >> 8) & 0x1FF | ((_WORD)v14 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v16, a3);
          sub_1413CA830(&v15, v16);
        }
        else
        {
          v15 = 124518401;
        }
        *(_DWORD *)(a1 + 36) = v15;
        break;
      default:
        return result;
    }
  }
  else if ( a2 > 1937007731 )
  {
    if ( a2 == 1937007732 )
    {
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
      if ( (__int64 *)*a3 == &qword_141B5C8A0 )
      {
        v13 = *((_DWORD *)a3 + 2);
        HIWORD(v15) = v13 >> 17;
        LOWORD(v15) = (v13 >> 8) & 0x1FF | ((_WORD)v13 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
      {
        (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v16, a3);
        sub_1413CA830(&v15, v16);
      }
      else
      {
        v15 = 124518401;
      }
      *(_DWORD *)(a1 + 32) = v15;
    }
    else
    {
      if ( a2 != 1954115685 )
        return result;
      *(_BYTE *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
  }
  else if ( a2 == 1835103331 )
  {
    *(_BYTE *)(a1 + 53) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  }
  else
  {
    if ( a2 != 1851880553 )
      return result;
    v6 = qword_141B5FE08;
    sub_140FE7960(v16, a3, 1315856756);
    v7 = sub_140F7A940(v6, v16);
    if ( v7 != 0 )
      *(_DWORD *)(a1 + 44) = *(_DWORD *)(v7 + 12);
    else
      *(_DWORD *)(a1 + 44) = -1;
  }
  return 1;
}

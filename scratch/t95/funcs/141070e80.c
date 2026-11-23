// THUNK ALIAS -> sub_143F0C310 (jmp:0x141070e80->0x143f0c310)
char __fastcall sub_143F0C310(__int64 a1, int a2, __int64 *a3)
{
  __int64 v5; // rbx
  unsigned int v7; // eax
  unsigned int v8; // eax
  __int64 v9; // rdx
  __int64 v10; // rdx
  __int64 v11; // rdx
  __int64 v12; // rdx
  int v13; // [rsp+28h] [rbp-30h] BYREF
  __int64 v14[5]; // [rsp+30h] [rbp-28h] BYREF

  switch ( a2 )
  {
    case 1313305444:
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          qword_141B5C8A0 = 0x141759DF8LL;
          byte_141B5C8A8 = 32;
          LOBYTE(v9) = 32;
          sub_1412EA280(&qword_141B5C8B0, v9);
          LOBYTE(v10) = 32;
          sub_1412EB230(&qword_141B5C8C0, v10);
          qword_141B5C8A0 = 0x141876208LL;
          qword_141B5C8B0 = 0x1418762E8LL;
          qword_141B5C8C0 = 0x141876308LL;
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      if ( (__int64 *)*a3 == &qword_141B5C8A0 )
      {
        v8 = *((_DWORD *)a3 + 2);
        HIWORD(v13) = v8 >> 17;
        LOWORD(v13) = (v8 >> 8) & 0x1FF | ((_WORD)v8 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*a3 + 160LL))(*a3, v14, a3);
        sub_1413CA830(&v13, v14);
      }
      else
      {
        v13 = 124518401;
      }
      *(_DWORD *)(a1 + 8) = v13;
      break;
    case 1313301860:
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          qword_141B5C8A0 = 0x141759DF8LL;
          byte_141B5C8A8 = 32;
          LOBYTE(v11) = 32;
          sub_1412EA280(&qword_141B5C8B0, v11);
          LOBYTE(v12) = 32;
          sub_1412EB230(&qword_141B5C8C0, v12);
          qword_141B5C8A0 = 0x141876208LL;
          qword_141B5C8B0 = 0x1418762E8LL;
          qword_141B5C8C0 = 0x141876308LL;
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      if ( (__int64 *)*a3 == &qword_141B5C8A0 )
      {
        v7 = *((_DWORD *)a3 + 2);
        HIWORD(v13) = v7 >> 17;
        LOWORD(v13) = (v7 >> 8) & 0x1FF | ((_WORD)v7 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*a3 + 160LL))(*a3, v14, a3);
        sub_1413CA830(&v13, v14);
      }
      else
      {
        v13 = 124518401;
      }
      *(_DWORD *)(a1 + 12) = v13;
      break;
    case 1313300839:
      v5 = qword_141B5FE60;
      sub_140FE7960((__int64)v14, a3, 0x6167726Du);
      *(_QWORD *)a1 = sub_140FA3700(v5, (int *)v14);
      break;
    default:
      return 0;
  }
  return 1;
}

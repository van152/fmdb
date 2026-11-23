// THUNK ALIAS -> sub_143C56D20 (jmp:0x140e882d0->0x143c56d20)
char __fastcall sub_143C56D20(__int64 a1, int a2, _QWORD *a3)
{
  __int64 v3; // rax
  __int64 v7; // rsi
  char result; // al
  __int64 v9; // rsi
  __int64 v10; // rsi
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rdi
  __int64 v14; // rsi
  __int64 v15; // rsi
  unsigned int v16; // eax
  int v17; // [rsp+48h] [rbp-30h] BYREF
  __int64 v18[5]; // [rsp+50h] [rbp-28h] BYREF

  v3 = *(_QWORD *)(a1 + 256);
  if ( v3 == 0 )
    return 0;
  if ( *(_QWORD *)(v3 + 120) == 0 )
  {
    if ( dword_141B5DAE8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5DAE8);
      if ( dword_141B5DAE8 == -1 )
      {
        sub_1407E53D0((unsigned int)&unk_141B5DA98, 1100140274, 1024, 24, 0, 0, 1024, 4096);
        sub_141751048(sub_140E9BAB0);
        sub_141750EA0(&dword_141B5DAE8);
      }
    }
    v7 = sub_1407E58C0(&unk_141B5DA98, 24);
    sub_141521AA0(v7, a1);
    *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL) = v7;
  }
  result = 0;
  if ( a2 <= 1130720631 )
  {
    switch ( a2 )
    {
      case 1130717796:
        v13 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
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
          v16 = *((_DWORD *)a3 + 2);
          HIWORD(v17) = v16 >> 17;
          LOWORD(v17) = (v16 >> 8) & 0x1FF | ((_WORD)v16 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, __int64 *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v18, a3);
          sub_1413CA830(&v17, v18);
        }
        else
        {
          v17 = 124518401;
        }
        *(_DWORD *)(v13 + 8) = v17;
        break;
      case 1130718068:
        v14 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
        *(_BYTE *)(v14 + 20) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        break;
      case 1130720622:
        v10 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
        *(_BYTE *)(v10 + 21) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        break;
      default:
        return result;
    }
  }
  else if ( a2 > 1130722411 )
  {
    if ( a2 == 1130722412 )
    {
      v15 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
      *(_BYTE *)(v15 + 18) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    else
    {
      if ( a2 != 1131246701 )
        return result;
      v11 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
      *(_BYTE *)(v11 + 19) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
  }
  else if ( a2 == 1130720632 )
  {
    v12 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
    *(_BYTE *)(v12 + 22) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  }
  else
  {
    if ( a2 != 1130721394 )
      return result;
    v9 = *(_QWORD *)(*(_QWORD *)(a1 + 256) + 120LL);
    *(_WORD *)(v9 + 16) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  }
  return 1;
}

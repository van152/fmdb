__int64 __fastcall sub_1413C40A0(char a1)
{
  __int64 v1; // rsi
  __int64 v2; // rax

  switch ( a1 )
  {
    case 0:
      if ( dword_141B63300 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B63300);
        if ( dword_141B63300 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B632B0,
            a2: 1100126312,
            a3: 1024,
            a4: 16,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5500);
          sub_141750EA0(a1: &dword_141B63300);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B632B0, a2: 16);
      *(_QWORD *)v1 = 0x1418B4858LL;
      *(_DWORD *)(v1 + 8) = 0;
      return v1;
    case 1:
      if ( dword_141B63358 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B63358);
        if ( dword_141B63358 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B63308,
            a2: 1100128997,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5680);
          sub_141750EA0(a1: &dword_141B63358);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B63308, a2: 24);
      *(_DWORD *)(v1 + 8) = 0;
      v2 = 0x1418B48D8LL;
      goto LABEL_15;
    case 2:
      if ( dword_141B633B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B633B0);
        if ( dword_141B633B0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B63360,
            a2: 1100131156,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5800);
          sub_141750EA0(a1: &dword_141B633B0);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B63360, a2: 24);
      *(_DWORD *)(v1 + 8) = 0;
      v2 = 0x1418B4968LL;
      goto LABEL_15;
    case 3:
      if ( dword_141B63460 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B63460);
        if ( dword_141B63460 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B63410,
            a2: 1100130169,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5C40);
          sub_141750EA0(a1: &dword_141B63460);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B63410, a2: 24);
      *(_DWORD *)(v1 + 8) = 0;
      *(_QWORD *)v1 = 0x1418B4A88LL;
      *(_DWORD *)(v1 + 16) = 0;
      *(_BYTE *)(v1 + 20) = 0;
      return v1;
    case 4:
      if ( dword_141B634B8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B634B8);
        if ( dword_141B634B8 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B63468,
            a2: 1100131192,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5DC0);
          sub_141750EA0(a1: &dword_141B634B8);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B63468, a2: 24);
      *(_DWORD *)(v1 + 8) = 0;
      *(_QWORD *)v1 = 0x1418B4B18LL;
      *(_WORD *)(v1 + 16) = -256;
      return v1;
    case 5:
      if ( dword_141B63510 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B63510);
        if ( dword_141B63510 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B634C0,
            a2: 1100131229,
            a3: 1024,
            a4: 24,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C5F40);
          sub_141750EA0(a1: &dword_141B63510);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B634C0, a2: 24);
      *(_DWORD *)(v1 + 8) = 0;
      v2 = 0x1418B4BA8LL;
LABEL_15:
      *(_QWORD *)v1 = v2;
      *(_WORD *)(v1 + 16) = 0;
      break;
    case 6:
      if ( dword_141B63408 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B63408);
        if ( dword_141B63408 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B633B8,
            a2: 1100130610,
            a3: 1024,
            a4: 40,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_1413C59B0);
          sub_141750EA0(a1: &dword_141B63408);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B633B8, a2: 40);
      *(_DWORD *)(v1 + 8) = 0;
      *(_QWORD *)v1 = 0x1418B49F8LL;
      if ( qword_141ABD470 == 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
          }
        }
        qword_141ABD470 = (__int64)&unk_141B59A68;
      }
      *(_QWORD *)(v1 + 32) = 0;
      *(_QWORD *)(v1 + 24) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      break;
    default:
      v1 = 0;
      break;
  }
  return v1;
}
